package com.emergencia.util;

import com.emergencia.model.Paciente;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Clase utilitaria para manejar la lectura y escritura de archivos.
 */
public class FileHandler {
    private static final Logger logger = LogManager.getLogger(FileHandler.class);

    /**
     * Lee un archivo de texto con información de pacientes.
     * Cada línea del archivo debe tener el formato: Nombre, Síntoma, Código
     *
     * @param filePath Ruta del archivo a leer
     * @return Lista de pacientes leídos del archivo
     */
    public static List<Paciente> loadPacientes(String filePath) {
        List<Paciente> pacientes = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) {
                    continue;  // Saltar líneas vacías
                }

                try {
                    // Dividir la línea por comas
                    String[] parts = line.split(",");

                    if (parts.length == 3) {
                        String nombre = parts[0].trim();
                        String sintoma = parts[1].trim();
                        char codigo = parts[2].trim().charAt(0);

                        pacientes.add(new Paciente(nombre, sintoma, codigo));
                    } else {
                        logger.warn("Formato incorrecto en línea: {}", line);
                    }
                } catch (Exception e) {
                    logger.error("Error al procesar línea: " + line, e);
                }
            }
        } catch (IOException e) {
            logger.error("Error al leer el archivo: " + filePath, e);
        }

        return pacientes;
    }
}
