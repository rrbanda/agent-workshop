package com.novacrest.mortgage.service;

import com.novacrest.mortgage.dto.ConditionUpdateRequest;
import com.novacrest.mortgage.dto.DocumentReviewRequest;
import com.novacrest.mortgage.exception.ResourceNotFoundException;
import com.novacrest.mortgage.model.CreditReport;
import com.novacrest.mortgage.model.MortgageApp;
import com.novacrest.mortgage.model.MortgageCondition;
import com.novacrest.mortgage.model.MortgageDocument;
import com.novacrest.mortgage.repository.CreditReportRepository;
import com.novacrest.mortgage.repository.MortgageAppRepository;
import com.novacrest.mortgage.repository.MortgageConditionRepository;
import com.novacrest.mortgage.repository.MortgageDocumentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Service
@Transactional
public class MortgageService {

    private static final Logger logger = LoggerFactory.getLogger(MortgageService.class);

    private final MortgageAppRepository appRepository;
    private final MortgageDocumentRepository documentRepository;
    private final MortgageConditionRepository conditionRepository;
    private final CreditReportRepository creditReportRepository;

    public MortgageService(MortgageAppRepository appRepository,
                           MortgageDocumentRepository documentRepository,
                           MortgageConditionRepository conditionRepository,
                           CreditReportRepository creditReportRepository) {
        this.appRepository = appRepository;
        this.documentRepository = documentRepository;
        this.conditionRepository = conditionRepository;
        this.creditReportRepository = creditReportRepository;
    }

    @Transactional(readOnly = true)
    public MortgageApp getApplicationById(Long id) {
        return appRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Mortgage application with ID " + id + " not found"));
    }

    @Transactional(readOnly = true)
    public MortgageApp getApplicationByNumber(String applicationNumber) {
        return appRepository.findByApplicationNumber(applicationNumber)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Mortgage application " + applicationNumber + " not found"));
    }

    @Transactional(readOnly = true)
    public List<MortgageApp> getApplicationsByCustomer(String customerId) {
        return appRepository.findByCustomerId(customerId);
    }

    @Transactional(readOnly = true)
    public List<MortgageCondition> getConditions(Long applicationId) {
        getApplicationById(applicationId);
        return conditionRepository.findByApplicationId(applicationId);
    }

    @Transactional(readOnly = true)
    public List<MortgageDocument> getDocuments(Long applicationId) {
        getApplicationById(applicationId);
        return documentRepository.findByApplicationId(applicationId);
    }

    public Map<String, Object> reviewDocument(Long documentId, DocumentReviewRequest request) {
        MortgageDocument document = documentRepository.findById(documentId)
                .orElseThrow(() -> new ResourceNotFoundException("Document with ID " + documentId + " not found"));

        MortgageDocument.DocumentStatus newStatus;
        try {
            newStatus = MortgageDocument.DocumentStatus.valueOf(request.status().toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Invalid status: " + request.status()
                    + ". Must be ACCEPTED or REJECTED");
        }

        document.setStatus(newStatus);
        document.setReviewedDate(LocalDateTime.now());

        if (newStatus == MortgageDocument.DocumentStatus.REJECTED && request.rejectionReason() != null) {
            document.setRejectionReason(request.rejectionReason());
        }

        documentRepository.save(document);
        logger.info("Document {} reviewed: status={}", document.getDocumentNumber(), newStatus);

        return Map.of(
                "success", true,
                "message", "Document " + document.getDocumentNumber() + " " + newStatus.name().toLowerCase(),
                "documentId", documentId,
                "status", newStatus.name()
        );
    }

    public Map<String, Object> updateCondition(Long conditionId, ConditionUpdateRequest request) {
        MortgageCondition condition = conditionRepository.findById(conditionId)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Condition with ID " + conditionId + " not found"));

        MortgageCondition.ConditionStatus newStatus;
        try {
            newStatus = MortgageCondition.ConditionStatus.valueOf(request.status().toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Invalid status: " + request.status()
                    + ". Must be SATISFIED, WAIVED, or PENDING_REVIEW");
        }

        condition.setStatus(newStatus);
        if (request.resolutionNotes() != null) {
            condition.setResolutionNotes(request.resolutionNotes());
        }

        conditionRepository.save(condition);
        logger.info("Condition {} updated: status={}", condition.getConditionNumber(), newStatus);

        return Map.of(
                "success", true,
                "message", "Condition " + condition.getConditionNumber() + " " + newStatus.name().toLowerCase(),
                "conditionId", conditionId,
                "status", newStatus.name()
        );
    }

    @Transactional(readOnly = true)
    public List<CreditReport> getCreditReports(String customerId) {
        return creditReportRepository.findByCustomerIdOrderByReportDateDesc(customerId);
    }

    public Map<String, Object> sendNotification(String customerId, String message, String channel) {
        String effectiveChannel = (channel != null && !channel.isBlank()) ? channel : "email";
        logger.info("Notification sent to customer {}: [{}] {}", customerId, effectiveChannel, message);

        return Map.of(
                "success", true,
                "message", "Notification sent to customer " + customerId + " via " + effectiveChannel,
                "customerId", customerId,
                "channel", effectiveChannel,
                "timestamp", LocalDateTime.now().toString()
        );
    }
}
