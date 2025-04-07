package com.emergencia.queue;

/**
 * Interfaz que define las operaciones básicas para una cola con prioridad.
 * @param <E> Tipo de elementos que se almacenarán en la cola, debe ser comparable.
 */
public interface PriorityQueue<E extends Comparable<E>> {

    /**
     * Agrega un elemento a la cola con prioridad.
     * @param element Elemento a agregar.
     */
    void add(E element);

    /**
     * Retorna el elemento con la mayor prioridad sin removerlo.
     * @return Elemento con mayor prioridad.
     * @throws java.util.NoSuchElementException si la cola está vacía.
     */
    E peek();

    /**
     * Retorna y remueve el elemento con la mayor prioridad.
     * @return Elemento con mayor prioridad.
     * @throws java.util.NoSuchElementException si la cola está vacía.
     */
    E remove();

    /**
     * Verifica si la cola está vacía.
     * @return true si la cola está vacía, false en caso contrario.
     */
    boolean isEmpty();

    /**
     * Retorna la cantidad de elementos en la cola.
     * @return Número de elementos en la cola.
     */
    int size();

    /**
     * Elimina todos los elementos de la cola.
     */
    void clear();
}
