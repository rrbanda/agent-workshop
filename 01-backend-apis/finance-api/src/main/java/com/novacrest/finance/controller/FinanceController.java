package com.novacrest.finance.controller;

import com.novacrest.finance.dto.*;
import com.novacrest.finance.entity.*;
import com.novacrest.finance.service.FinanceService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/finance")
@CrossOrigin(origins = "*")
@Tag(name = "Finance API", description = "REST API for order, invoice, dispute, and receipt management")
public class FinanceController {

    private static final Logger logger = LoggerFactory.getLogger(FinanceController.class);

    @Autowired
    private FinanceService financeService;
    
    @Operation(summary = "Get order history for a customer", description = "Retrieves the order history for a specific customer with optional date filtering and pagination", tags = {"Orders"})
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Order history retrieved successfully", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = Map.class))),
        @ApiResponse(responseCode = "400", description = "Bad request - Invalid input data"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @PostMapping(value = "/orders/history", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> getOrderHistory(@Parameter(description = "Order history request parameters", required = true) @Valid @RequestBody OrderHistoryRequest request) {
        logger.info("getOrderHistory called with request: {}", request);
        try {
            List<Order> orders = financeService.getOrderHistory(request);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Order history retrieved successfully");
            response.put("data", orders);
            response.put("count", orders.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Error retrieving order history: " + e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    @Operation(summary = "Get invoice history for a customer", description = "Retrieves the invoice history for a specific customer with optional date filtering and pagination", tags = {"Invoices"})
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Invoice history retrieved successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - Invalid input data"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @PostMapping(value = "/invoices/history", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> getInvoiceHistory(@Parameter(description = "Invoice history request parameters", required = true) @Valid @RequestBody InvoiceHistoryRequest request) {
        logger.info("getInvoiceHistory called with request: {}", request);
        try {
            List<Invoice> invoices = financeService.getInvoiceHistory(request);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Invoice history retrieved successfully");
            response.put("data", invoices);
            response.put("count", invoices.size());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Error retrieving invoice history: " + e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    @Operation(summary = "Start a duplicate charge dispute", description = "Creates a new dispute for a duplicate charge issue reported by a customer", tags = {"Disputes"})
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Duplicate charge dispute started successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - Invalid input data or business rule violation"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @PostMapping(value = "/disputes/duplicate-charge", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> startDuplicateChargeDispute(@Parameter(description = "Duplicate charge dispute request parameters", required = true) @Valid @RequestBody DuplicateChargeDisputeRequest request) {
        logger.info("startDuplicateChargeDispute called with request: {}", request);
        try {
            Dispute dispute = financeService.startDuplicateChargeDispute(request);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Duplicate charge dispute started successfully");
            response.put("data", dispute);
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (RuntimeException e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Error starting duplicate charge dispute: " + e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    @Operation(summary = "Find or regenerate a lost receipt", description = "Attempts to find an existing receipt or creates a new one for a lost receipt request", tags = {"Receipts"})
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Lost receipt found/created successfully"),
        @ApiResponse(responseCode = "400", description = "Bad request - Invalid input data or order not found"),
        @ApiResponse(responseCode = "500", description = "Internal server error")
    })
    @PostMapping(value = "/receipts/find-lost", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> findLostReceipt(@Parameter(description = "Find lost receipt request parameters", required = true) @Valid @RequestBody FindLostReceiptRequest request) {
        logger.info("findLostReceipt called with request: {}", request);
        try {
            Receipt receipt = financeService.findLostReceipt(request);
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Lost receipt found/created successfully");
            response.put("data", receipt);
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse);
        } catch (Exception e) {
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "Error finding lost receipt: " + e.getMessage());
            errorResponse.put("data", null);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    int count = 0;

    @Operation(summary = "Health check endpoint", description = "Returns the current health status of the Finance API service", tags = {"Health"})
    @ApiResponses(value = {@ApiResponse(responseCode = "200", description = "Service is healthy")})
    @GetMapping(value = "/health", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, Object>> healthCheck() {
        logger.info("healthCheck called");
        count++;
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "NovaCrest Finance API");
        response.put("count", count);
        response.put("timestamp", java.time.LocalDateTime.now());
        return ResponseEntity.ok(response);
    }
}
