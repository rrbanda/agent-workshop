package com.novacrest.mortgage.dto;

import jakarta.validation.constraints.NotBlank;

public record DocumentReviewRequest(
    @NotBlank(message = "Status is required (ACCEPTED or REJECTED)")
    String status,

    String rejectionReason
) {}
