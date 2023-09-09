package org.example.Services;

import com.example.qrpc.Hub;
import lombok.SneakyThrows;
import org.example.Controllers.ImageController;
import org.example.Models.Sensor;
import org.example.ProtoService.Client;
import org.example.Utils.SensorUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;


@Service
public class SensorService {

    private Client client = new Client();
    private SensorUtils utils = new SensorUtils();


    @Autowired
    private ImageController imageController;

    public Sensor getById(Integer id) {
        Hub.Sensor sensor = client.getSensorById(id);
        Sensor repoSensor = utils.toSensor(sensor);
        return repoSensor;
    }

    public List<Sensor> getAll() {
        List<Hub.Sensor> sensors = client.getAll();
        List<Sensor> repoSensors = utils.toSensor(sensors);
        return repoSensors;
    }

    @SneakyThrows
    public void changeGraph(long id, Long until, Long since) {
        imageController.executeScript(client.getValuesByTime(since,until,(int) id));
    }

    public List<Sensor> getAllByType(Hub.SensorType type) {
        return getAll().stream().filter(sensor -> sensor.getType().equals(type)).toList();
    }

}
