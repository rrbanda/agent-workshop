package com.novacrest.customer.exception;

public class DuplicateCustomerIdException extends RuntimeException {
    public DuplicateCustomerIdException(String message) {
        super(message);
    }
}
