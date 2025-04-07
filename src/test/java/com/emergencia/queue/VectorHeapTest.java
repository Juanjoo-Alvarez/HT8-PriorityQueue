package com.emergencia.queue;


import com.emergencia.model.Paciente;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Pruebas unitarias para la implementación de VectorHeap.
 */
public class VectorHeapTest {

    private VectorHeap<Integer> intHeap;
    private VectorHeap<Paciente> pacienteHeap;

    @BeforeEach
    public void setUp() {
        intHeap = new VectorHeap<>();
        pacienteHeap = new VectorHeap<>();
    }

    @Test
    public void testEmptyHeap() {
        assertTrue(intHeap.isEmpty());
        assertEquals(0, intHeap.size());
        assertThrows(NoSuchElementException.class, () -> intHeap.peek());
        assertThrows(NoSuchElementException.class, () -> intHeap.remove());
    }

    @Test
    public void testAddSingleElement() {
        intHeap.add(5);
        assertFalse(intHeap.isEmpty());
        assertEquals(1, intHeap.size());
        assertEquals(5, intHeap.peek());
    }

    @Test
    public void testAddMultipleElements() {
        intHeap.add(5);
        intHeap.add(3);
        intHeap.add(7);
        assertEquals(3, intHeap.size());
        assertEquals(3, intHeap.peek());
    }

    @Test
    public void testRemoveElements() {
        // Agregar elementos desordenados
        intHeap.add(5);
        intHeap.add(3);
        intHeap.add(7);
        intHeap.add(1);
        intHeap.add(9);

        // Verificar que se remueven en orden correcto (min-heap)
        assertEquals(1, intHeap.remove());
        assertEquals(3, intHeap.remove());
        assertEquals(5, intHeap.remove());
        assertEquals(7, intHeap.remove());
        assertEquals(9, intHeap.remove());

        // Verificar que el heap está vacío
        assertTrue(intHeap.isEmpty());
    }

    @Test
    public void testClear() {
        intHeap.add(5);
        intHeap.add(3);
        intHeap.add(7);

        intHeap.clear();

        assertTrue(intHeap.isEmpty());
        assertEquals(0, intHeap.size());
    }

    @Test
    public void testPacientePriority() {
        // Crear pacientes con diferentes prioridades
        Paciente pacienteC = new Paciente("Juan Perez", "Fractura de pierna", 'C');
        Paciente pacienteA = new Paciente("Maria Ramirez", "Apendicitis", 'A');
        Paciente pacienteE = new Paciente("Lorenzo Toledo", "Chikunguya", 'E');
        Paciente pacienteB = new Paciente("Carmen Sarmientos", "Dolores de parto", 'B');

        // Agregar pacientes en orden aleatorio
        pacienteHeap.add(pacienteC);
        pacienteHeap.add(pacienteA);
        pacienteHeap.add(pacienteE);
        pacienteHeap.add(pacienteB);

        // Verificar que se extraen en orden correcto de prioridad (A, B, C, E)
        assertEquals('A', pacienteHeap.remove().getCodigoEmergencia());
        assertEquals('B', pacienteHeap.remove().getCodigoEmergencia());
        assertEquals('C', pacienteHeap.remove().getCodigoEmergencia());
        assertEquals('E', pacienteHeap.remove().getCodigoEmergencia());
    }

    @Test
    public void testConstructorWithCollection() {
        // Crear una lista con elementos
        ArrayList<Integer> list = new ArrayList<>();
        list.add(5);
        list.add(3);
        list.add(7);
        list.add(1);
        list.add(9);

        // Crear un heap con la lista
        VectorHeap<Integer> heap = new VectorHeap<>(list);

        // Verificar que el heap se construyó correctamente
        assertEquals(5, heap.size());
        assertEquals(1, heap.remove());
        assertEquals(3, heap.remove());
        assertEquals(5, heap.remove());
        assertEquals(7, heap.remove());
        assertEquals(9, heap.remove());
    }

}