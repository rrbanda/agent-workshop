package com.novacrest.mortgage.dto;

import jakarta.validation.constraints.NotBlank;

public record NotificationRequest(
    @NotBlank(message = "Customer ID is required")
    String customerId,

    @NotBlank(message = "Message is required")
    String message,

    String channel
) {}
