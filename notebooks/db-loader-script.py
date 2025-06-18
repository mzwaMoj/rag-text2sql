# Metadata for [Ref].[CRS_CountryCode]
crs_countrycode_metadata = {
    "table": "[Ref].[CRS_CountryCode]",
    "columns": [
        {"name": "CountryShortCode", "type": "nvarchar(2)", "nullable": True},
        {"name": "Country", "type": "nvarchar(50)", "nullable": True},
        {"name": "Country2", "type": "nvarchar(50)", "nullable": True},
        {"name": "Country3", "type": "nvarchar(50)", "nullable": True},
    ]
}

# Metadata for [DATA].[CRS_GH_AccountReport]
crs_gh_accountreport_metadata = {
    "table": "[DATA].[CRS_GH_AccountReport]",
    "columns": [
        {"name": "ParentID", "type": "varchar(255)", "nullable": True},
        {"name": "DocTypeIndic2", "type": "varchar(255)", "nullable": True},
        {"name": "DocRefId3", "type": "varchar(255)", "nullable": True},
        {"name": "AccountNumber", "type": "varchar(255)", "nullable": True},
        {"name": "AccNumberType", "type": "varchar(255)", "nullable": True},
        {"name": "ClosedAccount", "type": "varchar(255)", "nullable": True},
        {"name": "DormantAccount", "type": "varchar(255)", "nullable": True},
        {"name": "UndocumentedAccount", "type": "varchar(255)", "nullable": True},
        {"name": "ResCountryCode4", "type": "varchar(255)", "nullable": True},
        {"name": "AcctHolderType", "type": "varchar(255)", "nullable": True},
        {"name": "nameType", "type": "varchar(255)", "nullable": True},
        {"name": "FirstName", "type": "varchar(255)", "nullable": True},
        {"name": "LastName", "type": "varchar(255)", "nullable": True},
        {"name": "MiddleName", "type": "varchar(255)", "nullable": True},
        {"name": "CountryCode5", "type": "varchar(255)", "nullable": True},
        {"name": "Street", "type": "varchar(255)", "nullable": True},
        {"name": "PostCode", "type": "varchar(255)", "nullable": True},
        {"name": "City", "type": "varchar(255)", "nullable": True},
        {"name": "BirthDate", "type": "varchar(255)", "nullable": True},
        {"name": "TIN6", "type": "varchar(255)", "nullable": True},
        {"name": "issuedBy7", "type": "varchar(255)", "nullable": True},
        {"name": "AccountBalance", "type": "varchar(255)", "nullable": True},
        {"name": "currCode", "type": "varchar(255)", "nullable": True},
        {"name": "Type", "type": "varchar(255)", "nullable": True},
        {"name": "PaymentAmnt", "type": "varchar(255)", "nullable": True},
        {"name": "currCode8", "type": "varchar(255)", "nullable": True},
        {"name": "Processed", "type": "bit", "nullable": True},
    ]
}

# Metadata for [DATA].[CRS_GH_MessageSpec]
crs_gh_messagespec_metadata = {
    "table": "[DATA].[CRS_GH_MessageSpec]",
    "columns": [
        {"name": "ParentID", "type": "varchar(255)", "nullable": True},
        {"name": "version", "type": "varchar(255)", "nullable": True},
        {"name": "SendingCompanyIN", "type": "varchar(255)", "nullable": True},
        {"name": "TransmittingCountry", "type": "varchar(255)", "nullable": True},
        {"name": "ReceivingCountry", "type": "varchar(255)", "nullable": True},
        {"name": "MessageType", "type": "varchar(255)", "nullable": True},
        {"name": "MessageRefId", "type": "varchar(255)", "nullable": True},
        {"name": "MessageTypeIndic", "type": "varchar(255)", "nullable": True},
        {"name": "ReportingPeriod", "type": "varchar(255)", "nullable": True},
        {"name": "Timestamp", "type": "varchar(255)", "nullable": True},
        {"name": "ResCountryCode", "type": "varchar(255)", "nullable": True},
        {"name": "TIN", "type": "varchar(255)", "nullable": True},
        {"name": "issuedBy", "type": "varchar(255)", "nullable": True},
        {"name": "Name", "type": "varchar(255)", "nullable": True},
        {"name": "CountryCode", "type": "varchar(255)", "nullable": True},
        {"name": "AddressFree", "type": "varchar(255)", "nullable": True},
        {"name": "DocTypeIndic", "type": "varchar(255)", "nullable": True},
        {"name": "DocRefId", "type": "varchar(255)", "nullable": True},
        {"name": "Processed", "type": "bit", "nullable": True},
    ]
}
