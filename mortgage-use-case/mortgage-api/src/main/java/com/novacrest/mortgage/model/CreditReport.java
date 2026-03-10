package com.novacrest.mortgage.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "credit_reports", indexes = {
    @Index(name = "idx_credit_customer_id", columnList = "customerId")
})
public class CreditReport {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id", nullable = false)
    @NotBlank
    private String customerId;

    @Column(name = "credit_score", nullable = false)
    @NotNull
    private Integer creditScore;

    @Column(name = "credit_bureau", nullable = false)
    @NotBlank
    private String creditBureau;

    @Column(name = "total_debt", precision = 12, scale = 2)
    private BigDecimal totalDebt;

    @Column(name = "monthly_obligations", precision = 10, scale = 2)
    private BigDecimal monthlyObligations;

    @Column(name = "derogatory_marks")
    private Integer derogatoryMarks;

    @Column(name = "total_accounts")
    private Integer totalAccounts;

    @Column(name = "open_accounts")
    private Integer openAccounts;

    @Column(name = "report_date", nullable = false)
    private LocalDateTime reportDate;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    public CreditReport() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }

    public Integer getCreditScore() { return creditScore; }
    public void setCreditScore(Integer creditScore) { this.creditScore = creditScore; }

    public String getCreditBureau() { return creditBureau; }
    public void setCreditBureau(String creditBureau) { this.creditBureau = creditBureau; }

    public BigDecimal getTotalDebt() { return totalDebt; }
    public void setTotalDebt(BigDecimal totalDebt) { this.totalDebt = totalDebt; }

    public BigDecimal getMonthlyObligations() { return monthlyObligations; }
    public void setMonthlyObligations(BigDecimal monthlyObligations) { this.monthlyObligations = monthlyObligations; }

    public Integer getDerogatoryMarks() { return derogatoryMarks; }
    public void setDerogatoryMarks(Integer derogatoryMarks) { this.derogatoryMarks = derogatoryMarks; }

    public Integer getTotalAccounts() { return totalAccounts; }
    public void setTotalAccounts(Integer totalAccounts) { this.totalAccounts = totalAccounts; }

    public Integer getOpenAccounts() { return openAccounts; }
    public void setOpenAccounts(Integer openAccounts) { this.openAccounts = openAccounts; }

    public LocalDateTime getReportDate() { return reportDate; }
    public void setReportDate(LocalDateTime reportDate) { this.reportDate = reportDate; }

    public LocalDateTime getCreatedAt() { return createdAt; }
}
