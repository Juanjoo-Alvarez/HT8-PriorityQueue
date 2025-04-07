package com.emergencia.queue;

import java.util.ArrayList;
import java.util.NoSuchElementException;

/**
 * Implementación de PriorityQueue usando un heap binario respaldado por ArrayList.
 * El elemento con el valor más pequeño según Comparable tendrá la mayor prioridad.
 *
 * @param <E> Tipo de elementos en la cola, deben ser comparables.
 */
public class VectorHeap<E extends Comparable<E>> implements PriorityQueue<E> {
    private ArrayList<E> heap; // El heap se almacena como un ArrayList

    /**
     * Constructor que inicializa un heap vacío.
     */
    public VectorHeap() {
        heap = new ArrayList<>();
    }

    /**
     * Constructor que inicializa el heap con los elementos de la colección dada.
     * @param elements Colección de elementos con que se inicializa el heap.
     */
    public VectorHeap(ArrayList<E> elements) {
        heap = new ArrayList<>(elements);
        // Heapify: reorganiza los elementos para mantener la propiedad de heap
        for (int i = parent(size()-1); i >= 0; i--) {
            percolateDown(i);
        }
    }

    /**
     * Calcula el índice del padre de un nodo.
     * @param index Índice del nodo hijo.
     * @return Índice del nodo padre.
     */
    private int parent(int index) {
        return (index - 1) / 2;
    }

    /**
     * Calcula el índice del hijo izquierdo de un nodo.
     * @param index Índice del nodo padre.
     * @return Índice del hijo izquierdo.
     */
    private int leftChild(int index) {
        return 2 * index + 1;
    }

    /**
     * Calcula el índice del hijo derecho de un nodo.
     * @param index Índice del nodo padre.
     * @return Índice del hijo derecho.
     */
    private int rightChild(int index) {
        return 2 * index + 2;
    }

    /**
     * Mueve un elemento hacia arriba en el heap hasta encontrar su posición correcta.
     * @param index Índice del elemento a mover.
     */
    private void percolateUp(int index) {
        E temp = heap.get(index);

        // Mientras no sea la raíz y el elemento tenga mayor prioridad que su padre
        while (index > 0 && temp.compareTo(heap.get(parent(index))) < 0) {
            // Mover el padre hacia abajo
            heap.set(index, heap.get(parent(index)));
            index = parent(index);
        }

        // Colocar el elemento en su posición final
        heap.set(index, temp);
    }

    /**
     * Mueve un elemento hacia abajo en el heap hasta encontrar su posición correcta.
     * @param index Índice del elemento a mover.
     */
    private void percolateDown(int index) {
        int child;
        E temp = heap.get(index);

        while (leftChild(index) < heap.size()) {
            child = leftChild(index);

            // Determinar cuál hijo tiene mayor prioridad
            if (child + 1 < heap.size() &&
                    heap.get(child + 1).compareTo(heap.get(child)) < 0) {
                child++;
            }

            // Si el elemento tiene mayor prioridad que ambos hijos, terminamos
            if (temp.compareTo(heap.get(child)) <= 0) {
                break;
            }

            // Mover el hijo con mayor prioridad hacia arriba
            heap.set(index, heap.get(child));
            index = child;
        }

        // Colocar el elemento en su posición final
        heap.set(index, temp);
    }

    /**
     * Agrega un elemento al heap manteniendo la propiedad del heap.
     * @param element Elemento a agregar.
     */
    @Override
    public void add(E element) {
        // Agregar al final del heap
        heap.add(element);
        // Reorganizar el heap
        percolateUp(heap.size() - 1);
    }

    /**
     * Retorna el elemento con la mayor prioridad sin removerlo.
     * @return Elemento con mayor prioridad.
     * @throws NoSuchElementException si el heap está vacío.
     */
    @Override
    public E peek() {
        if (isEmpty()) {
            throw new NoSuchElementException("Priority queue is empty");
        }
        return heap.get(0);
    }

    /**
     * Retorna y remueve el elemento con la mayor prioridad.
     * @return Elemento con mayor prioridad.
     * @throws NoSuchElementException si el heap está vacío.
     */
    @Override
    public E remove() {
        if (isEmpty()) {
            throw new NoSuchElementException("Priority queue is empty");
        }

        // Guardar el elemento de mayor prioridad (raíz)
        E result = heap.get(0);

        // Reemplazar la raíz con el último elemento
        E lastElement = heap.remove(heap.size() - 1);

        if (!heap.isEmpty()) {
            heap.set(0, lastElement);
            // Reorganizar el heap
            percolateDown(0);
        }

        return result;
    }

    /**
     * Verifica si el heap está vacío.
     * @return true si el heap está vacío, false en caso contrario.
     */
    @Override
    public boolean isEmpty() {
        return heap.isEmpty();
    }

    /**
     * Retorna el número de elementos en el heap.
     * @return Número de elementos.
     */
    @Override
    public int size() {
        return heap.size();
    }

    /**
     * Elimina todos los elementos del heap.
     */
    @Override
    public void clear() {
        heap.clear();
    }
}
