-- Seed data for NovaCrest Mortgage API
-- Applications are tied to existing NovaCrest customers (AROUT, LONEP, THECR, FRANR)

-- Mortgage Applications
INSERT INTO mortgage_applications (application_number, customer_id, property_address, loan_amount, loan_type, status, credit_score, annual_income, debt_to_income_ratio, created_at, updated_at) VALUES
('APP-001', 'AROUT', '742 Evergreen Terrace, Springfield, IL 62704', 320000.00, 'CONVENTIONAL', 'CONDITIONAL_APPROVAL', 715, 95000.00, 38.50, '2026-01-10 09:00:00', '2026-02-15 14:30:00'),
('APP-002', 'LONEP', '1600 Pennsylvania Ave, Washington, DC 20500', 450000.00, 'FHA', 'UNDERWRITING', 680, 120000.00, 42.00, '2026-01-20 10:30:00', '2026-02-20 11:00:00'),
('APP-003', 'THECR', '221B Baker Street, London, ON N6A 1B5', 275000.00, 'VA', 'SUBMITTED', 740, 88000.00, 31.00, '2026-02-01 08:15:00', '2026-02-05 09:00:00'),
('APP-004', 'FRANR', '350 Fifth Avenue, New York, NY 10118', 650000.00, 'JUMBO', 'DENIED', 580, 150000.00, 52.00, '2025-11-15 14:00:00', '2025-12-20 16:00:00');

-- Documents for APP-001 (AROUT - Conditional Approval, missing several docs)
INSERT INTO mortgage_documents (document_number, application_id, document_type, status, file_name, description, rejection_reason, document_date, requested_date, uploaded_date, reviewed_date, created_at, updated_at) VALUES
('DOC-001', 1, 'W2', 'REQUESTED', NULL, '2025 W-2 form from employer', NULL, NULL, '2026-02-15 14:30:00', NULL, NULL, '2026-02-15 14:30:00', '2026-02-15 14:30:00'),
('DOC-002', 1, 'BANK_STATEMENT', 'UPLOADED', 'arout_bank_aug2025.pdf', 'Bank of America checking account statement', NULL, '2025-08-01 00:00:00', '2026-02-15 14:30:00', '2026-02-18 09:15:00', NULL, '2026-02-15 14:30:00', '2026-02-18 09:15:00'),
('DOC-003', 1, 'PAY_STUB', 'ACCEPTED', 'arout_paystub_jan2026.pdf', 'January 2026 pay stub from Around the Horn Ltd', NULL, '2026-01-31 00:00:00', '2026-02-15 14:30:00', '2026-02-16 10:00:00', '2026-02-17 11:00:00', '2026-02-15 14:30:00', '2026-02-17 11:00:00'),
('DOC-004', 1, 'PROPERTY_APPRAISAL', 'REQUESTED', NULL, 'Independent property appraisal for 742 Evergreen Terrace', NULL, NULL, '2026-02-15 14:30:00', NULL, NULL, '2026-02-15 14:30:00', '2026-02-15 14:30:00'),
('DOC-005', 1, 'BANK_STATEMENT', 'REJECTED', 'arout_bank_dec2024.pdf', 'Bank of America checking account statement - December 2024', 'Statement is older than 60 days. Please provide a statement from the last 60 days.', '2024-12-01 00:00:00', '2026-02-15 14:30:00', '2026-02-19 08:00:00', '2026-02-19 15:00:00', '2026-02-15 14:30:00', '2026-02-19 15:00:00');

-- Documents for APP-002 (LONEP - Underwriting, all docs uploaded)
INSERT INTO mortgage_documents (document_number, application_id, document_type, status, file_name, description, rejection_reason, document_date, requested_date, uploaded_date, reviewed_date, created_at, updated_at) VALUES
('DOC-006', 2, 'W2', 'ACCEPTED', 'lonep_w2_2025.pdf', '2025 W-2 form', NULL, '2025-12-31 00:00:00', '2026-01-25 10:00:00', '2026-01-28 09:00:00', '2026-01-30 14:00:00', '2026-01-25 10:00:00', '2026-01-30 14:00:00'),
('DOC-007', 2, 'BANK_STATEMENT', 'ACCEPTED', 'lonep_bank_jan2026.pdf', 'January 2026 bank statement', NULL, '2026-01-31 00:00:00', '2026-01-25 10:00:00', '2026-02-02 11:00:00', '2026-02-03 10:00:00', '2026-01-25 10:00:00', '2026-02-03 10:00:00'),
('DOC-008', 2, 'PAY_STUB', 'ACCEPTED', 'lonep_paystub_jan2026.pdf', 'January 2026 pay stub', NULL, '2026-01-31 00:00:00', '2026-01-25 10:00:00', '2026-01-29 15:00:00', '2026-01-30 16:00:00', '2026-01-25 10:00:00', '2026-01-30 16:00:00'),
('DOC-009', 2, 'TAX_RETURN', 'ACCEPTED', 'lonep_tax_2024.pdf', '2024 federal tax return', NULL, '2025-04-15 00:00:00', '2026-01-25 10:00:00', '2026-01-30 13:00:00', '2026-02-01 09:00:00', '2026-01-25 10:00:00', '2026-02-01 09:00:00'),
('DOC-010', 2, 'PROPERTY_APPRAISAL', 'UPLOADED', 'lonep_appraisal.pdf', 'Property appraisal for 1600 Pennsylvania Ave', NULL, '2026-02-10 00:00:00', '2026-01-25 10:00:00', '2026-02-12 14:00:00', NULL, '2026-01-25 10:00:00', '2026-02-12 14:00:00');

-- Documents for APP-003 (THECR - VA loan, submitted)
INSERT INTO mortgage_documents (document_number, application_id, document_type, status, file_name, description, rejection_reason, document_date, requested_date, uploaded_date, reviewed_date, created_at, updated_at) VALUES
('DOC-011', 3, 'DD214', 'UPLOADED', 'thecr_dd214.pdf', 'DD-214 Certificate of Release or Discharge', NULL, '2020-06-15 00:00:00', '2026-02-01 08:15:00', '2026-02-03 10:00:00', NULL, '2026-02-01 08:15:00', '2026-02-03 10:00:00'),
('DOC-012', 3, 'CERTIFICATE_OF_ELIGIBILITY', 'UPLOADED', 'thecr_coe.pdf', 'VA Certificate of Eligibility', NULL, '2026-01-15 00:00:00', '2026-02-01 08:15:00', '2026-02-04 09:30:00', NULL, '2026-02-01 08:15:00', '2026-02-04 09:30:00');

-- Conditions for APP-001 (AROUT - 3 open conditions)
INSERT INTO mortgage_conditions (condition_number, application_id, description, required_document_type, status, resolution_notes, created_at, updated_at) VALUES
('COND-001', 1, 'Provide most recent W-2 form (2025) from current employer', 'W2', 'OPEN', NULL, '2026-02-15 14:30:00', '2026-02-15 14:30:00'),
('COND-002', 1, 'Provide bank statements from the last 60 days showing sufficient reserves', 'BANK_STATEMENT', 'OPEN', 'Previous submission (DOC-005) rejected - statement was older than 60 days', '2026-02-15 14:30:00', '2026-02-19 15:00:00'),
('COND-003', 1, 'Obtain independent property appraisal for 742 Evergreen Terrace', 'PROPERTY_APPRAISAL', 'OPEN', NULL, '2026-02-15 14:30:00', '2026-02-15 14:30:00');

-- Conditions for APP-002 (LONEP - 1 pending review)
INSERT INTO mortgage_conditions (condition_number, application_id, description, required_document_type, status, resolution_notes, created_at, updated_at) VALUES
('COND-004', 2, 'Property appraisal must confirm value meets or exceeds loan amount', 'PROPERTY_APPRAISAL', 'PENDING_REVIEW', 'Appraisal document uploaded, awaiting review', '2026-01-25 10:00:00', '2026-02-12 14:00:00');

-- Credit Reports
INSERT INTO credit_reports (customer_id, credit_score, credit_bureau, total_debt, monthly_obligations, derogatory_marks, total_accounts, open_accounts, report_date, created_at) VALUES
('AROUT', 715, 'Experian', 45000.00, 2850.00, 0, 12, 5, '2026-01-08 10:00:00', '2026-01-08 10:00:00'),
('AROUT', 710, 'TransUnion', 45200.00, 2875.00, 0, 11, 5, '2026-01-08 10:00:00', '2026-01-08 10:00:00'),
('LONEP', 680, 'Experian', 62000.00, 4100.00, 1, 15, 8, '2026-01-18 09:00:00', '2026-01-18 09:00:00'),
('LONEP', 675, 'Equifax', 63500.00, 4200.00, 1, 14, 7, '2026-01-18 09:00:00', '2026-01-18 09:00:00'),
('THECR', 740, 'Experian', 28000.00, 1800.00, 0, 8, 4, '2026-01-30 11:00:00', '2026-01-30 11:00:00'),
('FRANR', 580, 'TransUnion', 95000.00, 6200.00, 3, 20, 12, '2025-11-10 14:00:00', '2025-11-10 14:00:00');
