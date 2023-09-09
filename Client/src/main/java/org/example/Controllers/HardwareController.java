package org.example.Controllers;

import com.example.qrpc.Hub;
import lombok.SneakyThrows;
import org.example.Services.HardwareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HardwareController {

    @Autowired
    HardwareService hardwareService;


    @SneakyThrows
    @GetMapping("/sensors/control")
    public String getSensors(Model model) {
       /* model.addAttribute("sensors",hardwareService.getAllByType(Hub.SensorType.HUMIDITY_SENSOR));
        model.addAttribute("sensors",hardwareService.getAllByType(Hub.SensorType.LIGHT_SENSOR));
        model.addAttribute("sensors",hardwareService.getAllByType(Hub.SensorType.TEMPERATURE_SENSOR));*/
       // return "controlPage";
        return "main";
    }
}
