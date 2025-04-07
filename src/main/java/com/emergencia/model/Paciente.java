package com.emergencia.model;

/**
 * Clase que representa a un paciente en la sala de emergencias.
 * Implementa Comparable para poder ser ordenado por prioridad.
 */
public class Paciente implements Comparable<Paciente> {
    private String nombre;
    private String sintoma;
    private char codigoEmergencia; // A, B, C, D, E (donde A es la mayor prioridad)

    /**
     * Constructor de la clase Paciente.
     * @param nombre Nombre del paciente.
     * @param sintoma Descripción del síntoma.
     * @param codigoEmergencia Código de emergencia (A-E).
     */
    public Paciente(String nombre, String sintoma, char codigoEmergencia) {
        this.nombre = nombre;
        this.sintoma = sintoma;
        this.codigoEmergencia = Character.toUpperCase(codigoEmergencia);
    }

    /**
     * Obtiene el nombre del paciente.
     * @return Nombre del paciente.
     */
    public String getNombre() {
        return nombre;
    }

    /**
     * Obtiene el síntoma del paciente.
     * @return Síntoma del paciente.
     */
    public String getSintoma() {
        return sintoma;
    }

    /**
     * Obtiene el código de emergencia del paciente.
     * @return Código de emergencia (A-E).
     */
    public char getCodigoEmergencia() {
        return codigoEmergencia;
    }

    /**
     * Compara este paciente con otro para ordenarlos por prioridad.
     * Las prioridades van de A (mayor) a E (menor).
     * @param other Otro paciente para comparar.
     * @return Valor negativo si este paciente tiene mayor prioridad,
     *         positivo si tiene menor prioridad, 0 si tienen la misma prioridad.
     */
    @Override
    public int compareTo(Paciente other) {
        // Comparamos los códigos directamente ya que A < B < C < D < E en ASCII
        return Character.compare(this.codigoEmergencia, other.codigoEmergencia);
    }

    /**
     * Representación de texto del paciente.
     * @return Cadena con la información del paciente.
     */
    @Override
    public String toString() {
        return nombre + ", " + sintoma + ", " + codigoEmergencia;
    }
}