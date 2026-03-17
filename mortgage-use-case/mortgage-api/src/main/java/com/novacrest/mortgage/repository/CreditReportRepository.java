package com.novacrest.mortgage.repository;

import com.novacrest.mortgage.model.CreditReport;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CreditReportRepository extends JpaRepository<CreditReport, Long> {

    List<CreditReport> findByCustomerIdOrderByReportDateDesc(String customerId);
}
