package org.example.Utils;

import com.example.qrpc.Hub;
import org.example.Models.Sensor;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

public class SensorUtils {


    public Sensor toSensor(Hub.Sensor sensor) {
        Sensor repoSensor = new Sensor();
        repoSensor.setID(sensor.getSensorId());
        repoSensor.setValue(sensor.getValue());
        repoSensor.setName(sensor.getSensorName());
        repoSensor.setType(sensor.getSensorType());
        repoSensor.setTimestamp(new Timestamp(sensor.getTimestamp()));
        ColorsUtils.setColor(repoSensor);
        return repoSensor;
    }

    public List<Sensor> toSensor(List<Hub.Sensor> sensors) {
        List<Sensor> repoSensors = new ArrayList<>();
        for (Hub.Sensor sensor: sensors) {
            Sensor repoSensor = new Sensor();
            repoSensor.setID(sensor.getSensorId());
            repoSensor.setValue(sensor.getValue());
            repoSensor.setName(sensor.getSensorName());
            repoSensor.setType(sensor.getSensorType());
            System.out.println("from client "+ sensor.getTimestamp());
            repoSensor.setTimestamp(new Timestamp(sensor.getTimestamp()));
            ColorsUtils.setColor(repoSensor);
            repoSensors.add(repoSensor);
        }
        return repoSensors;
    }
}
