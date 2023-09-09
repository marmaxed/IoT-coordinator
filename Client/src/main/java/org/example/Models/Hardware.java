package org.example.Models;

import com.example.qrpc.Hub;
import lombok.Data;
import javax.persistence.Entity;
import javax.persistence.Id;

@Data
@Entity
public class Hardware {

    @Id
    private Integer ID;
    private Hub.SensorType type;
    private String color;
    private Boolean state;

}

