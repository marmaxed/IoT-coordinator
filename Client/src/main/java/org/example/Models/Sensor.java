package org.example.Models;


import com.example.qrpc.Hub;
import javax.persistence.*;
import lombok.Data;
import java.sql.Timestamp;

@Data
@Entity
@Table(name="sensors")
public class Sensor {

    @Id
    @Column(name = "id", nullable = false)
    private Integer ID;
    @Id
    @Column(name = "date")
    private Timestamp timestamp;
    @Enumerated(EnumType.STRING)
    @Column(name="type")
    private Hub.SensorType type;
    @Column(name="name")
    private String name;
    @Column(name = "value")
    private float value;
    private String color;


}
