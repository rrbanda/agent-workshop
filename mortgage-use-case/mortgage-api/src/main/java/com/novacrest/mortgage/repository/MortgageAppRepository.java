package com.novacrest.mortgage.repository;

import com.novacrest.mortgage.model.MortgageApp;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface MortgageAppRepository extends JpaRepository<MortgageApp, Long> {

    Optional<MortgageApp> findByApplicationNumber(String applicationNumber);

    List<MortgageApp> findByCustomerId(String customerId);

    List<MortgageApp> findByStatus(MortgageApp.ApplicationStatus status);
}
