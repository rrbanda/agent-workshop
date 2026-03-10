package com.novacrest.mortgage.controller;

import com.novacrest.mortgage.dto.ConditionUpdateRequest;
import com.novacrest.mortgage.dto.DocumentReviewRequest;
import com.novacrest.mortgage.dto.NotificationRequest;
import com.novacrest.mortgage.model.MortgageApp;
import com.novacrest.mortgage.model.MortgageCondition;
import com.novacrest.mortgage.model.MortgageDocument;
import com.novacrest.mortgage.model.CreditReport;
import com.novacrest.mortgage.service.MortgageService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/mortgage")
@Tag(name = "Mortgage", description = "Mortgage application processing and document management")
public class MortgageController {

    private static final Logger logger = LoggerFactory.getLogger(MortgageController.class);

    private final MortgageService mortgageService;

    public MortgageController(MortgageService mortgageService) {
        this.mortgageService = mortgageService;
    }

    @GetMapping("/applications/{id}")
    @Operation(summary = "Get mortgage application by ID")
    public ResponseEntity<MortgageApp> getApplication(@PathVariable Long id) {
        logger.info("Getting application by ID: {}", id);
        return ResponseEntity.ok(mortgageService.getApplicationById(id));
    }

    @GetMapping("/applications")
    @Operation(summary = "Search mortgage applications by customer ID")
    public ResponseEntity<Map<String, Object>> searchApplications(
            @RequestParam String customerId) {
        logger.info("Searching applications for customer: {}", customerId);
        List<MortgageApp> apps = mortgageService.getApplicationsByCustomer(customerId);
        return ResponseEntity.ok(Map.of(
                "success", true,
                "data", apps,
                "count", apps.size()
        ));
    }

    @GetMapping("/applications/{id}/conditions")
    @Operation(summary = "List conditions for a mortgage application")
    public ResponseEntity<Map<String, Object>> getConditions(@PathVariable Long id) {
        logger.info("Getting conditions for application: {}", id);
        List<MortgageCondition> conditions = mortgageService.getConditions(id);
        return ResponseEntity.ok(Map.of(
                "success", true,
                "data", conditions,
                "count", conditions.size()
        ));
    }

    @GetMapping("/applications/{id}/documents")
    @Operation(summary = "List documents for a mortgage application")
    public ResponseEntity<Map<String, Object>> getDocuments(@PathVariable Long id) {
        logger.info("Getting documents for application: {}", id);
        List<MortgageDocument> documents = mortgageService.getDocuments(id);
        return ResponseEntity.ok(Map.of(
                "success", true,
                "data", documents,
                "count", documents.size()
        ));
    }

    @PostMapping("/documents/{id}/review")
    @Operation(summary = "Accept or reject a document")
    public ResponseEntity<Map<String, Object>> reviewDocument(
            @PathVariable Long id,
            @Valid @RequestBody DocumentReviewRequest request) {
        logger.info("Reviewing document {}: status={}", id, request.status());
        return ResponseEntity.ok(mortgageService.reviewDocument(id, request));
    }

    @PutMapping("/conditions/{id}")
    @Operation(summary = "Update condition status")
    public ResponseEntity<Map<String, Object>> updateCondition(
            @PathVariable Long id,
            @Valid @RequestBody ConditionUpdateRequest request) {
        logger.info("Updating condition {}: status={}", id, request.status());
        return ResponseEntity.ok(mortgageService.updateCondition(id, request));
    }

    @GetMapping("/credit-reports")
    @Operation(summary = "Get credit report for a customer")
    public ResponseEntity<Map<String, Object>> getCreditReports(
            @RequestParam String customerId) {
        logger.info("Getting credit reports for customer: {}", customerId);
        List<CreditReport> reports = mortgageService.getCreditReports(customerId);
        return ResponseEntity.ok(Map.of(
                "success", true,
                "data", reports,
                "count", reports.size()
        ));
    }

    @PostMapping("/notifications")
    @Operation(summary = "Send notification to a borrower")
    public ResponseEntity<Map<String, Object>> sendNotification(
            @Valid @RequestBody NotificationRequest request) {
        logger.info("Sending notification to customer: {}", request.customerId());
        return ResponseEntity.ok(mortgageService.sendNotification(
                request.customerId(), request.message(), request.channel()));
    }

    @GetMapping("/health")
    @Operation(summary = "Health check")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP", "service", "mortgage-api"));
    }
}
