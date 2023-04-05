using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;

public class UDPListen : MonoBehaviour
{
    private UdpClient udpClient;
    public Material view_material;
    Texture2D sphere_texture = null;
    // Start is called before the first frame update
    byte[] jpegData=null;
    void Start()
    {
        sphere_texture = new Texture2D(1, 1, TextureFormat.RGBA32, false, true);
        sphere_texture.wrapMode = TextureWrapMode.Clamp;

        udpClient = new UdpClient(4000);
        udpClient.JoinMulticastGroup(IPAddress.Parse("239.255.0.1"));

        udpClient.BeginReceive(OnReceived, udpClient);

        Debug.Log("Start");

    }
    private void OnReceived(System.IAsyncResult result)
    {
        UdpClient getUdp = (UdpClient)result.AsyncState;
        IPEndPoint ipEnd = null;

        jpegData = getUdp.EndReceive(result, ref ipEnd);
        getUdp.BeginReceive(OnReceived, getUdp);


    }
    // Update is called once per frame
    void Update()
    {
        if (jpegData == null) return;
        bool isOK = sphere_texture.LoadImage(jpegData, true);
        jpegData = null;

        if(!(view_material.mainTexture == sphere_texture))
        {
            view_material.mainTexture = sphere_texture;
        }
        
    }
}
