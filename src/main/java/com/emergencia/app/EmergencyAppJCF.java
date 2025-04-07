package com.emergencia.app;

import com.emergencia.model.Paciente;
import com.emergencia.util.FileHandler;

import java.util.List;
import java.util.PriorityQueue;
import java.util.Scanner;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Aplicación principal para la gestión de emergencias usando PriorityQueue del Java Collection Framework.
 */
public class EmergencyAppJCF {
    private static final Logger logger = LogManager.getLogger(EmergencyAppJCF.class);

    public static void main(String[] args) {
        logger.info("Iniciando Sistema de Atención de Emergencias (JCF)");

        // Cargar pacientes desde archivo
        String filePath = "src/main/resources/pacientes.txt";
        List<Paciente> pacientesList = FileHandler.loadPacientes(filePath);

        if (pacientesList.isEmpty()) {
            logger.error("No se pudieron cargar pacientes desde el archivo. Finalizando programa.");
            return;
        }

        // Crear cola de prioridad con la implementación de Java Collection Framework
        PriorityQueue<Paciente> emergencyQueue = new PriorityQueue<>();

        // Agregar pacientes a la cola
        for (Paciente paciente : pacientesList) {
            emergencyQueue.add(paciente);
            logger.info("Paciente registrado: {}", paciente);
        }

        System.out.println("=======================================================");
        System.out.println("  SISTEMA DE ATENCIÓN DE EMERGENCIAS HOSPITALARIAS");
        System.out.println("     (Usando Java Collection Framework)");
        System.out.println("=======================================================");
        System.out.println("Total de pacientes en espera: " + emergencyQueue.size());
        System.out.println("-------------------------------------------------------");

        // Interfaz para atender pacientes
        Scanner scanner = new Scanner(System.in);
        while (!emergencyQueue.isEmpty()) {
            System.out.println("\nOpciones:");
            System.out.println("1. Atender siguiente paciente");
            System.out.println("2. Ver número de pacientes en espera");
            System.out.println("3. Salir");
            System.out.print("Seleccione una opción: ");

            if (scanner.hasNextInt()) {
                int option = scanner.nextInt();
                scanner.nextLine(); // Consumir el salto de línea

                switch (option) {
                    case 1:
                        atenderPaciente(emergencyQueue);
                        break;
                    case 2:
                        System.out.println("Pacientes en espera: " + emergencyQueue.size());
                        break;
                    case 3:
                        System.out.println("Finalizando programa...");
                        return;
                    default:
                        System.out.println("Opción no válida. Intente de nuevo.");
                }
            } else {
                System.out.println("Entrada no válida. Intente de nuevo.");
                scanner.nextLine(); // Limpiar la entrada inválida
            }
        }

        System.out.println("\nTodos los pacientes han sido atendidos.");
        scanner.close();
    }

    /**
     * Atiende al siguiente paciente en la cola de prioridad.
     * @param queue Cola de prioridad de pacientes.
     */
    private static void atenderPaciente(PriorityQueue<Paciente> queue) {
        if (queue.isEmpty()) {
            System.out.println("No hay pacientes en espera.");
            return;
        }

        Paciente paciente = queue.poll();

        System.out.println("\n-------------------------------------------------------");
        System.out.println("ATENDIENDO PACIENTE:");
        System.out.println("Nombre: " + paciente.getNombre());
        System.out.println("Síntoma: " + paciente.getSintoma());
        System.out.println("Prioridad: " + paciente.getCodigoEmergencia());
        System.out.println("-------------------------------------------------------");

        logger.info("Paciente atendido: {}", paciente);
    }
}
