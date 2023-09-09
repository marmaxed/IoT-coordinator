package org.example.ProtoService;

import com.example.qrpc.Hub;
import com.example.qrpc.HubInfoServiceGrpc;
import io.grpc.Channel;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import java.io.File;
import java.util.List;
import java.util.Map;

import io.grpc.netty.shaded.io.grpc.netty.GrpcSslContexts;
import io.grpc.netty.shaded.io.grpc.netty.NettyChannelBuilder;
import io.grpc.netty.shaded.io.netty.handler.ssl.SslContext;
import lombok.SneakyThrows;

import javax.net.ssl.SSLException;

public class Client {

    public static io.grpc.netty.shaded.io.netty.handler.ssl.SslContext loadTLSCredentials() throws SSLException {
        File serverCACertFile = null;
        File clientCertFile = null;
        File clientKeyFile = null;
        try {
           serverCACertFile = new File("C:\\IotClient\\src\\main\\resources\\cert\\ca-cert.pem");
           clientCertFile = new File("C:\\IotClient\\src\\main\\resources\\cert\\client-cert.pem");
           clientKeyFile = new File("C:\\IotClient\\src\\main\\resources\\cert\\client-key.pem");
            System.out.println("first");
        } catch (Exception e) {

        }
        try {
            System.out.println("second");
            return GrpcSslContexts.forClient()
                    .keyManager(clientCertFile, clientKeyFile)
                    .trustManager(serverCACertFile)
                    .build();
        } catch (Exception e) {
            System.out.println("second");
            return null;
        }
    }
    public static ManagedChannel sslChannel() throws SSLException {
        System.out.println("fifth");
        return  NettyChannelBuilder.forAddress("192.168.0.106",6789)
                .sslContext(loadTLSCredentials())
                .build();
    }

    static Channel channel = ManagedChannelBuilder.forTarget("localhost:6789").usePlaintext().build();

    public static ManagedChannel simpleChannel(){
        return ManagedChannelBuilder.forAddress("192.168.0.106", 6789)
                .usePlaintext()
                .build();
    }
    public static HubInfoServiceGrpc.HubInfoServiceBlockingStub myStub = HubInfoServiceGrpc.newBlockingStub(channel);

   /* static {
        try {
            myStub = HubInfoServiceGrpc.newBlockingStub(simpleChannel());
        } catch (SSLException e) {
            throw new RuntimeException(e);
        }
    }*/

    public Hub.Sensor getSensorById(Integer id) {
        Hub.SensorDataRequest request = Hub.SensorDataRequest.newBuilder().setSensorId(id).build();
        Hub.SensorDataResponse response = myStub.getSensorData(request);
        return response.getSensor();
    }

    public Object[] getValuesByTime(long since, long until, int id) {
        Hub.TimeRequest request = Hub.TimeRequest.newBuilder().setSince(since).setUntil(until).setSensorId(id).build();
        Hub.TimeResponse response = myStub.getValuesByTimeStamp(request);
        Object[] obj = new Object[2];
        obj[0] = response.getTimeList();
        obj[1] = response.getValueList();
        return obj;
    }

    public List<Hub.Sensor> getSensorsByIDs(List<Integer> ids) {
        Hub.SensorsDataRequest request = Hub.SensorsDataRequest.newBuilder().addAllSensorIds(ids).build();
        Hub.SensorsDataResponse response = myStub.getSensorsData(request);
        return response.getSensorListList();
    }

    public List<Hub.Sensor> getAll() {
        Hub.AllSensorsDataRequest request = Hub.AllSensorsDataRequest.newBuilder().build();
        Hub.AllSensorsDataResponse response = myStub.getAllSensorsData(request);
        return response.getSensorsList();
    }

    public Map<Integer, Hub.SensorType> getTypes() {
        Hub.AllSensorsListRequest request = Hub.AllSensorsListRequest.newBuilder().build();
        Hub.AllSensorsListResponse response = myStub.getAllSensorsList(request);
        return response.getSensorListMap();
    }

    public void changeState() {
        Hub.AllSensorsListRequest request = Hub.AllSensorsListRequest.newBuilder().build();
        Hub.AllSensorsListResponse response = myStub.getAllSensorsList(request);
    }
}
