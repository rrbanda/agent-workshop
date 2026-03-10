CREATE TABLE IF NOT EXISTS mortgage_applications (
    id BIGSERIAL PRIMARY KEY,
    application_number VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    property_address VARCHAR(500) NOT NULL,
    loan_amount DECIMAL(12,2) NOT NULL CHECK (loan_amount > 0),
    loan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    credit_score INTEGER,
    annual_income DECIMAL(12,2),
    debt_to_income_ratio DECIMAL(5,2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mortgage_documents (
    id BIGSERIAL PRIMARY KEY,
    document_number VARCHAR(255) UNIQUE NOT NULL,
    application_id BIGINT NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    file_name VARCHAR(255),
    description TEXT,
    rejection_reason TEXT,
    document_date TIMESTAMP,
    requested_date TIMESTAMP,
    uploaded_date TIMESTAMP,
    reviewed_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES mortgage_applications(id)
);

CREATE TABLE IF NOT EXISTS mortgage_conditions (
    id BIGSERIAL PRIMARY KEY,
    condition_number VARCHAR(255) UNIQUE NOT NULL,
    application_id BIGINT NOT NULL,
    description TEXT NOT NULL,
    required_document_type VARCHAR(50),
    status VARCHAR(50) NOT NULL,
    resolution_notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES mortgage_applications(id)
);

CREATE TABLE IF NOT EXISTS credit_reports (
    id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    credit_score INTEGER NOT NULL,
    credit_bureau VARCHAR(100) NOT NULL,
    total_debt DECIMAL(12,2),
    monthly_obligations DECIMAL(10,2),
    derogatory_marks INTEGER,
    total_accounts INTEGER,
    open_accounts INTEGER,
    report_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_app_customer_id ON mortgage_applications(customer_id);
CREATE INDEX IF NOT EXISTS idx_app_status ON mortgage_applications(status);
CREATE INDEX IF NOT EXISTS idx_app_number ON mortgage_applications(application_number);
CREATE INDEX IF NOT EXISTS idx_doc_application_id ON mortgage_documents(application_id);
CREATE INDEX IF NOT EXISTS idx_doc_status ON mortgage_documents(status);
CREATE INDEX IF NOT EXISTS idx_doc_type ON mortgage_documents(document_type);
CREATE INDEX IF NOT EXISTS idx_cond_application_id ON mortgage_conditions(application_id);
CREATE INDEX IF NOT EXISTS idx_cond_status ON mortgage_conditions(status);
CREATE INDEX IF NOT EXISTS idx_credit_customer_id ON credit_reports(customer_id);
