package com.novacrest.mortgage.repository;

import com.novacrest.mortgage.model.MortgageCondition;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MortgageConditionRepository extends JpaRepository<MortgageCondition, Long> {

    List<MortgageCondition> findByApplicationId(Long applicationId);

    List<MortgageCondition> findByApplicationIdAndStatus(Long applicationId, MortgageCondition.ConditionStatus status);
}
