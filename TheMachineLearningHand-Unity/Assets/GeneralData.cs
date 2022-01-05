using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading;
using System.Net.Sockets;
using Debug = UnityEngine.Debug;
using System.Windows.Input;

public class GeneralData : MonoBehaviour
{
    private static bool ready = false;
    private static List<HingeJoint> sortedAllHingeJoints;

    // Start is called before the first frame update
    void Start()
    {
    }

    public static bool isReady()
    {
        if (ready)
        {
            return true;
        }

        // Object fetching related logic
        HingeJoint[] allHingeObjects = FindObjectsOfType(
            typeof(HingeJoint)) as HingeJoint[]; // Should return all the finger limbs (since they have joints)
        sortedAllHingeJoints = allHingeObjects.OrderBy(go => go.name).ToList();

        ready = true;
        return ready;
    }

    public static UnityEngine.GameObject[] getHingeLimbs(string rootName)
    {
        // Sifts through the hinged objects to determine the ones we want
        var sortedHingeJoints = new ArrayList();
        foreach (var hinge in sortedAllHingeJoints)
        {
            if (GeneralData.isAncestor(hinge.transform, rootName) == true)
            {
                sortedHingeJoints.Add(hinge);
            }
        }

        // Retrieves the movable limbs
        UnityEngine.GameObject[] movableLimbs = new GameObject[sortedHingeJoints.Count];
        for (int i = 0; i < sortedHingeJoints.Count; i++)
        {
            movableLimbs[i] = ((HingeJoint) sortedHingeJoints[i]).gameObject;
        }

        return movableLimbs;
    }


    /**
     * Splits the string into float array where elements are divided by a space (' ')
     */
    public static float[] string2floatArray(string original)
    {
        string[] stringData = original.Split(' ');
        float[] floatArrayData = new float[stringData.Length];

        for (int i = 0; i < stringData.Length; i++)
        {
            floatArrayData[i] = (float) (double.Parse(stringData[i])); //, System.Globalization.NumberStyles.Float);
        }

        return floatArrayData;
    }

    /**
     * Recursively goes through the ancestors of the object to find if it has the specified parent.
     */
    public static bool isAncestor(Transform inQuestion, string name)
    {
        if (inQuestion.parent == null)
        {
            return false;
        }

        if (inQuestion.parent.name.Equals(name))
        {
            return true;
        }
        else
        {
            return isAncestor(inQuestion.parent, name);
        }
    }

    public static float rads2degrees(float radians)
    {
        return (float) (radians / Math.PI * 180);
    }
}