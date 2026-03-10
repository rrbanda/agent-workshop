package com.novacrest.mortgage.dto;

import jakarta.validation.constraints.NotBlank;

public record ConditionUpdateRequest(
    @NotBlank(message = "Status is required (SATISFIED, WAIVED, or PENDING_REVIEW)")
    String status,

    String resolutionNotes
) {}
