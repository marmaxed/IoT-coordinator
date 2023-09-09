package org.example.Services;

import com.example.qrpc.Hub;
import org.example.Models.Hardware;
import org.example.Models.Sensor;
import org.example.ProtoService.Client;
import org.example.Utils.SensorUtils;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class HardwareService {

    /*  private Client client = new Client();
    private SensorUtils utils = new SensorUtils();

    public List<Sensor> getAll() {
        List<Hub.Hardware> hardware = client.getAllHardware();
        List<Hardware> webHardware = utils.toHardware(hardware);
        return webHardware;
    }

    public List<Sensor> getAllByType(Hub.SensorType type) {
        return getAll().stream().filter(hardware -> hardware.getType().equals(type)).toList();
    }*/

}
