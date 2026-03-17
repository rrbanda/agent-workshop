package com.novacrest.mortgage.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "mortgage_conditions", indexes = {
    @Index(name = "idx_cond_application_id", columnList = "applicationId"),
    @Index(name = "idx_cond_status", columnList = "status")
})
public class MortgageCondition {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "condition_number", unique = true, nullable = false)
    @NotBlank
    private String conditionNumber;

    @Column(name = "application_id", nullable = false)
    @NotNull
    private Long applicationId;

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    @NotBlank
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(name = "required_document_type")
    private MortgageDocument.DocumentType requiredDocumentType;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private ConditionStatus status;

    @Column(name = "resolution_notes", columnDefinition = "TEXT")
    private String resolutionNotes;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    public enum ConditionStatus {
        OPEN, SATISFIED, WAIVED, PENDING_REVIEW
    }

    public MortgageCondition() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getConditionNumber() { return conditionNumber; }
    public void setConditionNumber(String conditionNumber) { this.conditionNumber = conditionNumber; }

    public Long getApplicationId() { return applicationId; }
    public void setApplicationId(Long applicationId) { this.applicationId = applicationId; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public MortgageDocument.DocumentType getRequiredDocumentType() { return requiredDocumentType; }
    public void setRequiredDocumentType(MortgageDocument.DocumentType requiredDocumentType) { this.requiredDocumentType = requiredDocumentType; }

    public ConditionStatus getStatus() { return status; }
    public void setStatus(ConditionStatus status) { this.status = status; }

    public String getResolutionNotes() { return resolutionNotes; }
    public void setResolutionNotes(String resolutionNotes) { this.resolutionNotes = resolutionNotes; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}
