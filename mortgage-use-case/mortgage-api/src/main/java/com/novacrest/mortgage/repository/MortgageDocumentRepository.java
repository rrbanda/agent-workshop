package com.novacrest.mortgage.repository;

import com.novacrest.mortgage.model.MortgageDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MortgageDocumentRepository extends JpaRepository<MortgageDocument, Long> {

    List<MortgageDocument> findByApplicationId(Long applicationId);

    List<MortgageDocument> findByApplicationIdAndStatus(Long applicationId, MortgageDocument.DocumentStatus status);

    List<MortgageDocument> findByApplicationIdAndDocumentType(Long applicationId, MortgageDocument.DocumentType documentType);
}
