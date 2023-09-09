package org.example.Controllers;

import com.example.qrpc.Hub;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.SneakyThrows;
import org.example.Services.SensorService;
import org.example.Utils.TimeUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import javax.script.ScriptException;
import java.io.FileNotFoundException;
import java.io.IOException;

@Controller
public class SensorsController {

    @Autowired
    private SensorService sensorService;

    @Autowired
    private ImageController imageController;

    @SneakyThrows
    @GetMapping("/sensors")
    public String getSensors(Model model) {
        model.addAttribute("humidity",sensorService.getAllByType(Hub.SensorType.HUMIDITY_SENSOR));
        model.addAttribute("temperature",sensorService.getAllByType(Hub.SensorType.TEMPERATURE_SENSOR));
        model.addAttribute("light",sensorService.getAllByType(Hub.SensorType.LIGHT_SENSOR));
        return "main";
    }

    @GetMapping("/sensors/{id}")
    public String getSensor(@PathVariable Integer id, Model model) {
        model.addAttribute("sensor",sensorService.getById(id));
        model.addAttribute("state",true);
        return "sensorPage";
    }

    @PostMapping("/sensors/{id}")
    public String changeGraph(@PathVariable Integer id,Model model, @RequestParam(name="until") String until,@RequestParam(name="u_h") Integer u_h,
            @RequestParam(name = "u_m") Integer u_m,@RequestParam(name="since") String since,@RequestParam(name="s_h") Integer s_h,
                              @RequestParam(name = "s_m") Integer s_m) throws ScriptException, FileNotFoundException {
        long start = TimeUtils.getTime(since,s_h,s_m);
        long end = TimeUtils.getTime(until,u_h,u_m);
        if (start<end) {
            model.addAttribute("alert","Данные не коректны");
            model.addAttribute("sensor",sensorService.getById(id));
            model.addAttribute("state",true);
            return "sensorPage";
        }
        sensorService.changeGraph(id,start,end);
        model.addAttribute("sensor",sensorService.getById(id));
        model.addAttribute("state",true);
        return "sensorPage";
    }

    @GetMapping("/someservlet")
    public void testReq(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
        String text = "some text";
        System.out.println("here");
        response.setContentType("text/plain");  // Set content type of the response so that jQuery knows what it can expect.
        response.setCharacterEncoding("UTF-8"); // You want world domination, huh?
        response.getWriter().write(text);
    }

}
