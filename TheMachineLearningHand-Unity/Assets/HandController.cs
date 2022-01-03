using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading;
using System.Net.Sockets;
using System.Threading.Tasks;
using Debug = UnityEngine.Debug;
using System.Windows.Input;
using NUnit.Compatibility;

public class HandController : MonoBehaviour
{
    // Game variables
    private UnityEngine.GameObject[] movableLimbs;
    private UnityEngine.Rigidbody[] rigidBodies;
    private float[] limb_velocities; // velocity that should be applied in radians
    private float[] limbData; // angular. Position in degrees, velocity in radians

    // Server constants
    public const String SERVER_HOST = "127.0.0.1";
    public const int SERVER_PORT = 5001;
    public IPEndPoint serverEndPoint = new IPEndPoint(IPAddress.Parse(SERVER_HOST), SERVER_PORT);

    // Process variables
    private UdpClient connection;

    // Start is called before the first frame update
    void Start()
    {
        // Object fetching related logic
        print("Started the hand controller.");
        while (GeneralData.isReady() == false)
        {
        }

        movableLimbs = GeneralData.getHingeLimbs("Hand Real");
        rigidBodies = new Rigidbody[movableLimbs.Length];
        limb_velocities = new float[movableLimbs.Length];
        limbData = new float[movableLimbs.Length * 2];

        for (int i = 0; i < movableLimbs.Length; i++)
        {
            rigidBodies[i] = ((GameObject) movableLimbs[i]).GetComponent(typeof(Rigidbody)) as Rigidbody;
            rigidBodies[i].maxAngularVelocity = 12;
        }

        print("Started the threads. Detected " + movableLimbs.Length.ToString() + " controllable limbs.");

        // Creates and starts the client
        connection = new UdpClient(SERVER_HOST, SERVER_PORT);
        connection.DontFragment = true;
    }

    /*
 * GetStringTorques
 * Organizes the retrieval of the unity hand angles between the main and logic thread.
 */
    private string GetStringLimbData_forThread()
    {
        string stringLimbData = "";

        for (int i = 0; i < limbData.Length; i++)
        {
            float angle = limbData[i];

            if (i % 2 == 0) // Only converts angular position from degrees to radians
            {
                angle = angle > 180 ? angle - 360 : angle;
                angle *= 0.01745329252f;
            }

            stringLimbData += angle.ToString() + " ";
        }

        stringLimbData = stringLimbData.TrimEnd(' ');
        return stringLimbData;
    }

    private void FixedUpdate()
    {
        // // TODO, Duplicate code here, figure this out later
        // float[] minAngle = new float[] {0, 0, 0};
        // float[] maxAngle = new float[] {70, 70, 60};
        //
        // for (int i = 0; i < movableLimbs.Length; i++)
        // {
        //     float angle = movableLimbs[i].transform.localEulerAngles.x;
        //     angle = angle > 180 ? angle - 360 : angle;
        //
        //     float velocity = (float) (GeneralData.rads2degrees(rigidBodies[i].angularVelocity.x) * Time.fixedDeltaTime);
        //
        //     if (i == 0 && angle + velocity > 35) // TODO, thumb exception, deal with this properly later
        //     {
        //         movableLimbs[i].transform.localEulerAngles = new Vector3(35, 0, 0);
        //         rigidBodies[i].angularVelocity = Vector3.zero;
        //         limb_velocities[i] = 0;
        //     }
        //     else if (angle + velocity < minAngle[i % 3])
        //     {
        //         movableLimbs[i].transform.localEulerAngles = new Vector3(minAngle[i % 3], 0, 0);
        //         rigidBodies[i].angularVelocity = Vector3.zero;
        //         limb_velocities[i] = 0;
        //     }
        //     else if (angle + velocity > maxAngle[i % 3])
        //     {
        //         movableLimbs[i].transform.localEulerAngles = new Vector3(maxAngle[i % 3], 0, 0);
        //         rigidBodies[i].angularVelocity = Vector3.zero;
        //         limb_velocities[i] = 0;
        //     }
        // }
    }

    // Update is called once per frame
    void Update()
    {
        // Retrieves the limb velocity data from the server
        if (connection.Available > 0)
        {
            try
            {
                byte[] datagram = connection.Receive(ref serverEndPoint);
                string datagramDecoded = System.Text.Encoding.UTF8.GetString(datagram);
                limb_velocities = GeneralData.string2floatArray(datagramDecoded);
                Console.Write(limb_velocities.ToString());
            }
            catch (Exception e)
            {
                // Console.WriteLine(e);
                // throw;
            }
        }

        // Continuously records and applies existing velocities to the limbs
        float[] minAngle = new float[] {0, 0, 0};
        float[] maxAngle = new float[] {70, 70, 60};
        // float[] maxAngle = new float[] {110, 110, 100};

        for (int i = 0; i < movableLimbs.Length; i++)
        {
            float angle = movableLimbs[i].transform.localEulerAngles.x;
            angle = angle > 180 ? angle - 360 : angle;

            // Applies the computed velocities to the hand
            if (i == 0 && angle > 35) // TODO, thumb exception, deal with this properly later
            {
                movableLimbs[i].transform.localEulerAngles = new Vector3(35, 0, 0);
                rigidBodies[i].angularVelocity = Vector3.zero;
                limb_velocities[i] = 0;
            }
            else if (angle < minAngle[i % 3])
            {
                movableLimbs[i].transform.localEulerAngles = new Vector3(minAngle[i % 3], 0, 0);
                rigidBodies[i].angularVelocity = Vector3.zero;
                limb_velocities[i] = 0;
            }
            else if (angle > maxAngle[i % 3])
            {
                movableLimbs[i].transform.localEulerAngles = new Vector3(maxAngle[i % 3], 0, 0);
                rigidBodies[i].angularVelocity = Vector3.zero;
                limb_velocities[i] = 0;
            }
            else if (i % 3 == 0)
            {
                // Applies the current velocity to the proximal limb (its velocity is not relative to metacarpal bone)
                rigidBodies[i].angularVelocity = new Vector3(limb_velocities[i], 0, 0);
            }
            else
            {
                // Make the velocity the sum of the given and parent velocity
                rigidBodies[i].angularVelocity =
                    new Vector3(
                        movableLimbs[i].transform.parent.GetComponent<Rigidbody>().angularVelocity.x +
                        limb_velocities[i], 0, 0);
            }

            // Records the new limb data to send to the Python Script
            limbData[i * 2] = angle;
            limbData[i * 2 + 1] = rigidBodies[i].angularVelocity.x;
        }


        // Sends the data to the server
        try
        {
            byte[] dataToSend = System.Text.Encoding.UTF8.GetBytes(GetStringLimbData_forThread());
            connection.Send(dataToSend, dataToSend.Length);
        }
        catch (Exception e)
        {
            // Console.WriteLine(e);
            // throw;
        }
    }

    private void OnDestroy()
    {
        connection.Close();
        print("Stopped.");
    }
}