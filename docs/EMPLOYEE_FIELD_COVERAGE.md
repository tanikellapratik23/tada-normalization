# Employee field inventory

This report distinguishes common semantic mappings from lossless provider extensions. Extensions are not claimed as normalized equivalents. Every received field is also preserved in `source_record`. Array element schemas are listed even when synthetic arrays are empty. Regenerate with `python scripts/build_mapping_report.py`.

## prismhr

Source: `contracts/prismhr/openapi/prismhr-2025.09.openapi.json#/components/schemas/Employee`

| Source path | Destination / treatment |
| --- | --- |
| `id` | `data.source_id + scoped identity` |
| `lastName` | `data.profile.last_name` |
| `firstName` | `data.profile.first_name` |
| `middleInitial` | `data.profile.middle_name` |
| `preferredName` | `data.profile.preferred_name` |
| `person.ethnicCode` | `data.profile.ethnicity_code` |
| `person.birthDate` | `data.profile.birth_date` |
| `person.driverLicenseId` | `extensions (provider-specific, unchanged)` |
| `person.cobraSSN` | `extensions (provider-specific, unchanged)` |
| `person.employerIds[]` | `extensions (provider-specific, unchanged)` |
| `person.cobraOnly` | `extensions (provider-specific, unchanged)` |
| `person.geoCode` | `extensions (provider-specific, unchanged)` |
| `person.maritalStatus` | `data.profile.marital_status_code` |
| `person.marriedDate` | `extensions (provider-specific, unchanged)` |
| `person.smoker` | `extensions (provider-specific, unchanged)` |
| `person.peoStartDate` | `extensions (provider-specific, unchanged)` |
| `person.handicapped` | `data.profile.disability_code` |
| `person.blind` | `extensions (provider-specific, unchanged)` |
| `person.veteran` | `data.profile.veteran_code` |
| `person.vietnamVet` | `extensions (provider-specific, unchanged)` |
| `person.disabledVet` | `extensions (provider-specific, unchanged)` |
| `person.hrpCitizenshipCountry` | `data.profile.citizenship_country` |
| `person.deceased` | `data.profile.deceased` |
| `person.gender` | `data.profile.gender_code` |
| `person.taxZipCode` | `extensions (provider-specific, unchanged)` |
| `person.highlyCompensated` | `extensions (provider-specific, unchanged)` |
| `person.keyEmployee` | `extensions (provider-specific, unchanged)` |
| `person.overrideGeoCode` | `extensions (provider-specific, unchanged)` |
| `person.overrideGeoEndDate` | `extensions (provider-specific, unchanged)` |
| `person.nickname` | `extensions (provider-specific, unchanged)` |
| `person.deceasedDate` | `data.profile.deceased_date` |
| `person.driverState` | `extensions (provider-specific, unchanged)` |
| `person.driverLicenseExpireDate` | `extensions (provider-specific, unchanged)` |
| `person.driverLicenseClass` | `extensions (provider-specific, unchanged)` |
| `person.ohioFormC112` | `extensions (provider-specific, unchanged)` |
| `person.unincorporatedResidence` | `extensions (provider-specific, unchanged)` |
| `person.w2AddressLine1` | `extensions (provider-specific, unchanged)` |
| `person.w2AddressLine2` | `extensions (provider-specific, unchanged)` |
| `person.w2City` | `extensions (provider-specific, unchanged)` |
| `person.w2State` | `extensions (provider-specific, unchanged)` |
| `person.w2PostalCode` | `extensions (provider-specific, unchanged)` |
| `person.w2ElecForm` | `extensions (provider-specific, unchanged)` |
| `person.w2ElecFormDate` | `extensions (provider-specific, unchanged)` |
| `person.legacyEmployeeId` | `extensions (provider-specific, unchanged)` |
| `person.hispanic` | `extensions (provider-specific, unchanged)` |
| `person.agricultureWorker` | `extensions (provider-specific, unchanged)` |
| `person.otherProtectedVet` | `extensions (provider-specific, unchanged)` |
| `person.activeDutyBadgeVet` | `extensions (provider-specific, unchanged)` |
| `person.recentlySeparatedVet` | `extensions (provider-specific, unchanged)` |
| `person.serviceMedalVet` | `extensions (provider-specific, unchanged)` |
| `person.preferredLanguage` | `data.profile.language` |
| `person.emergencyContact[].contactName` | `data.emergency_contacts[].contactName` |
| `person.emergencyContact[].contactInfo` | `data.emergency_contacts[].contactInfo` |
| `person.emergencyContact[].contactRelationship` | `data.emergency_contacts[].contactRelationship` |
| `person.emergencyContact[].contactType` | `data.emergency_contacts[].contactType` |
| `person.userId` | `extensions (provider-specific, unchanged)` |
| `person.autoPolicies[].autoInsurancePolicyId` | `extensions (provider-specific, unchanged)` |
| `person.autoPolicies[].autoInsuranceCarrierName` | `extensions (provider-specific, unchanged)` |
| `person.autoPolicies[].autoInsuranceHolderName` | `extensions (provider-specific, unchanged)` |
| `person.autoPolicies[].autoInsurancePolicyStartDate` | `extensions (provider-specific, unchanged)` |
| `person.autoPolicies[].autoInsurancePolicyExpDate` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleMake` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleModel` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleYear` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleAddDate` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleRemoveDate` | `extensions (provider-specific, unchanged)` |
| `person.vehicleDetails[].vehicleRegNo` | `extensions (provider-specific, unchanged)` |
| `person.personChecksum` | `extensions (provider-specific, unchanged)` |
| `contactInformation.addressLine1` | `data.address.line1` |
| `contactInformation.addressLine2` | `data.address.line2` |
| `contactInformation.city` | `data.address.city` |
| `contactInformation.state` | `data.address.region` |
| `contactInformation.zipcode` | `data.address.postal_code` |
| `contactInformation.zipSuffix` | `data.address.postal_suffix` |
| `contactInformation.county` | `extensions (provider-specific, unchanged)` |
| `contactInformation.schoolDistrict` | `extensions (provider-specific, unchanged)` |
| `contactInformation.homePhone` | `data.contact.home_phone` |
| `contactInformation.mobilePhone` | `data.contact.mobile_phone` |
| `contactInformation.emailAddress` | `data.contact.email` |
| `client.employeeStatus` | `data.employment.status_code` |
| `client.statusClass` | `data.employment.status` |
| `client.statusDate` | `data.employment.status_date` |
| `client.employeeType` | `data.employment.type_code` |
| `client.typeClass` | `extensions (provider-specific, unchanged)` |
| `client.typeDate` | `extensions (provider-specific, unchanged)` |
| `client.transferInfo[].transferStatus` | `extensions (provider-specific, unchanged)` |
| `client.transferInfo[].transferEmployeeId` | `extensions (provider-specific, unchanged)` |
| `client.transferInfo[].transferClientId` | `extensions (provider-specific, unchanged)` |
| `client.transferInfo[].transferDate` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertyCode` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertyIssueDate` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertySerialNumber` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertyValue` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertyReturnDate` | `extensions (provider-specific, unchanged)` |
| `client.property[].propertyComment` | `extensions (provider-specific, unchanged)` |
| `client.hawaiiMedWaivers[].medWaiverYear` | `extensions (provider-specific, unchanged)` |
| `client.hawaiiMedWaivers[].medWaiverReason` | `extensions (provider-specific, unchanged)` |
| `client.jobCode` | `data.job.code` |
| `client.jobStartDate` | `data.job.start_date` |
| `client.firstHireDate` | `data.employment.first_hire_date` |
| `client.lastHireDate` | `data.employment.hire_date` |
| `client.flsaExempt` | `data.job.flsa_exempt` |
| `client.cafeteriaPlan[].planAmt` | `extensions (provider-specific, unchanged)` |
| `client.cafeteriaPlan[].planEffectiveDate` | `extensions (provider-specific, unchanged)` |
| `client.seniorityDate` | `data.employment.seniority_date` |
| `client.officer` | `extensions (provider-specific, unchanged)` |
| `client.workCompOfficer` | `extensions (provider-specific, unchanged)` |
| `client.scorpOwner` | `extensions (provider-specific, unchanged)` |
| `client.businessOwner` | `extensions (provider-specific, unchanged)` |
| `client.termReasonCode` | `data.employment.termination_reason_code` |
| `client.termExplanation` | `data.employment.termination_explanation` |
| `client.lastStatusChangeDate` | `extensions (provider-specific, unchanged)` |
| `client.lastJobChangeDate` | `extensions (provider-specific, unchanged)` |
| `client.newHireReportDate` | `extensions (provider-specific, unchanged)` |
| `client.employee1099` | `data.employment.contractor` |
| `client.clientEmployeeId` | `data.employment.employee_number` |
| `client.clockNum` | `extensions (provider-specific, unchanged)` |
| `client.primaryEmailSource` | `extensions (provider-specific, unchanged)` |
| `client.benefitEmail` | `extensions (provider-specific, unchanged)` |
| `client.rehireOk` | `extensions (provider-specific, unchanged)` |
| `client.returnDate` | `data.employment.return_date` |
| `client.workPhone` | `data.contact.work_phone` |
| `client.workPhoneExt` | `data.contact.work_phone_extension` |
| `client.probationDate` | `data.employment.probation_date` |
| `client.courtOrderMedical` | `extensions (provider-specific, unchanged)` |
| `client.childSpouseSupport` | `extensions (provider-specific, unchanged)` |
| `client.childSpouseArrears` | `extensions (provider-specific, unchanged)` |
| `client.addressLine1` | `data.mailing_address.line1` |
| `client.addressLine2` | `data.mailing_address.line2` |
| `client.city` | `data.mailing_address.city` |
| `client.state` | `data.mailing_address.region` |
| `client.zip` | `data.mailing_address.postal_code` |
| `client.zipSuffix` | `extensions (provider-specific, unchanged)` |
| `client.handbookMailDate` | `extensions (provider-specific, unchanged)` |
| `client.handbookRecvDate` | `extensions (provider-specific, unchanged)` |
| `client.unionCode` | `data.organization.union_code` |
| `client.unionDate` | `extensions (provider-specific, unchanged)` |
| `client.subCostCenter` | `extensions (provider-specific, unchanged)` |
| `client.electronicOnboard` | `extensions (provider-specific, unchanged)` |
| `client.electronicOnboardDate` | `extensions (provider-specific, unchanged)` |
| `client.reportsTo` | `extensions (provider-specific, unchanged)` |
| `client.onboardInProgress` | `extensions (provider-specific, unchanged)` |
| `client.backgroundTest` | `extensions (provider-specific, unchanged)` |
| `client.backgroundTestDate` | `extensions (provider-specific, unchanged)` |
| `client.workersCompExempt` | `extensions (provider-specific, unchanged)` |
| `client.genderDesignation` | `extensions (provider-specific, unchanged)` |
| `client.preferredPronoun` | `data.profile.pronouns` |
| `client.clientChecksum` | `extensions (provider-specific, unchanged)` |
| `client.homeLocation` | `data.organization.location_code` |
| `client.homeDivision` | `data.organization.division_code` |
| `client.homeDepartment` | `data.organization.department_code` |
| `client.workShift` | `data.organization.shift_code` |
| `client.projCostCenter` | `extensions (provider-specific, unchanged)` |
| `client.workGroupCode` | `data.organization.work_group_code` |
| `client.benefitGroup` | `data.organization.benefit_group_code` |
| `client.retirementBenefitGroup` | `extensions (provider-specific, unchanged)` |
| `client.workEmail` | `data.contact.work_email` |
| `client.electronic1095C` | `extensions (provider-specific, unchanged)` |
| `client.manager` | `data.organization.manager_source_id` |
| `client.selfIdDisabilityForm` | `extensions (provider-specific, unchanged)` |
| `client.applicantId` | `extensions (provider-specific, unchanged)` |
| `compensation.ssn` | `extensions (provider-specific, unchanged)` |
| `compensation.payGroup` | `data.compensation.pay_group` |
| `compensation.payPeriod` | `data.compensation.pay_period_code` |
| `compensation.payPeriodInfo[].periodCode` | `extensions (provider-specific, unchanged)` |
| `compensation.payPeriodInfo[].periodBase` | `extensions (provider-specific, unchanged)` |
| `compensation.defaultHours` | `extensions (provider-specific, unchanged)` |
| `compensation.payMethod` | `data.compensation.basis` |
| `compensation.allocationTemplateId` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].locationCode` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].percent` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].job` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].deptCode` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].project` | `extensions (provider-specific, unchanged)` |
| `compensation.payAllocation[].division` | `extensions (provider-specific, unchanged)` |
| `compensation.standardHours` | `data.compensation.standard_hours` |
| `compensation.stateTax[].stateCode` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].nonResCertFiled` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].filingStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].primaryAllowance` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].secondaryAllowance` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].exemptAmount` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].supplExemptAmount` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].overrideType` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].overrideAmount` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].reduceAddlWithholding` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].fixedWithholding` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].alternateCalc` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].stateW4Filed` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].stateW4Year` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].multipleJobs` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].dependents` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].otherIncome` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].deductions` | `extensions (provider-specific, unchanged)` |
| `compensation.stateTax[].nonResCertYear` | `extensions (provider-specific, unchanged)` |
| `compensation.hourlyPay` | `data.compensation.hourly_rate` |
| `compensation.salary` | `data.compensation.period_salary` |
| `compensation.workShift` | `extensions (provider-specific, unchanged)` |
| `compensation.paidThruDate` | `extensions (provider-specific, unchanged)` |
| `compensation.eicFileStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.fedFilingStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.fedWithholdAllowance` | `extensions (provider-specific, unchanged)` |
| `compensation.fedOverrideType` | `extensions (provider-specific, unchanged)` |
| `compensation.fedOverrideAmt` | `extensions (provider-specific, unchanged)` |
| `compensation.fedTaxCalc` | `extensions (provider-specific, unchanged)` |
| `compensation.fedMultipleJobs` | `extensions (provider-specific, unchanged)` |
| `compensation.fedDependents` | `extensions (provider-specific, unchanged)` |
| `compensation.fedOtherIncome` | `extensions (provider-specific, unchanged)` |
| `compensation.fedDeductions` | `extensions (provider-specific, unchanged)` |
| `compensation.hourlyPayRate` | `data.compensation.basis_rate` |
| `compensation.hourlyPayPeriod` | `data.compensation.basis_rate_period_code` |
| `compensation.deliverCheckHome` | `extensions (provider-specific, unchanged)` |
| `compensation.autoAcceptTimeSheet` | `extensions (provider-specific, unchanged)` |
| `compensation.longPayTable` | `extensions (provider-specific, unchanged)` |
| `compensation.longBasisDate` | `extensions (provider-specific, unchanged)` |
| `compensation.annualPay` | `data.compensation.annual_salary` |
| `compensation.effectiveDate` | `data.compensation.effective_date` |
| `compensation.localTax[].authId` | `extensions (provider-specific, unchanged)` |
| `compensation.localTax[].filingStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.localTax[].primaryAllowance` | `extensions (provider-specific, unchanged)` |
| `compensation.localTax[].nonResCert` | `extensions (provider-specific, unchanged)` |
| `compensation.localTax[].addlWithheld` | `extensions (provider-specific, unchanged)` |
| `compensation.lastChangePct` | `extensions (provider-specific, unchanged)` |
| `compensation.lastChangeAmt` | `extensions (provider-specific, unchanged)` |
| `compensation.lastPayDate` | `data.compensation.last_pay_date` |
| `compensation.quartile` | `extensions (provider-specific, unchanged)` |
| `compensation.compaRatio` | `extensions (provider-specific, unchanged)` |
| `compensation.benefitsBasePay` | `extensions (provider-specific, unchanged)` |
| `compensation.perDiemPay` | `extensions (provider-specific, unchanged)` |
| `compensation.taxCreditEmp` | `extensions (provider-specific, unchanged)` |
| `compensation.autoPayCode` | `extensions (provider-specific, unchanged)` |
| `compensation.altPayRate[]` | `extensions (provider-specific, unchanged)` |
| `compensation.pensionStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.profitSharing` | `extensions (provider-specific, unchanged)` |
| `compensation.eeImage[].masterId` | `extensions (provider-specific, unchanged)` |
| `compensation.eeImage[].verifyDateTime` | `extensions (provider-specific, unchanged)` |
| `compensation.eeImage[].verifyUserId` | `extensions (provider-specific, unchanged)` |
| `compensation.wagePlanCA` | `extensions (provider-specific, unchanged)` |
| `compensation.perfReviewLastDate` | `extensions (provider-specific, unchanged)` |
| `compensation.perfReviewNextDate` | `extensions (provider-specific, unchanged)` |
| `compensation.i9imageAudit[].auditDate` | `extensions (provider-specific, unchanged)` |
| `compensation.i9imageAudit[].auditUser` | `extensions (provider-specific, unchanged)` |
| `compensation.i9imageAudit[].auditId` | `extensions (provider-specific, unchanged)` |
| `compensation.i9imageAudit[].auditStep` | `extensions (provider-specific, unchanged)` |
| `compensation.perfReviewLastRating` | `extensions (provider-specific, unchanged)` |
| `compensation.compReviewNextDate` | `extensions (provider-specific, unchanged)` |
| `compensation.perfReviewLastTitle` | `extensions (provider-specific, unchanged)` |
| `compensation.fedW5Year` | `extensions (provider-specific, unchanged)` |
| `compensation.fedW5Filed` | `extensions (provider-specific, unchanged)` |
| `compensation.fedW4Filed` | `extensions (provider-specific, unchanged)` |
| `compensation.fedW4Year` | `extensions (provider-specific, unchanged)` |
| `compensation.lockIns[].state` | `extensions (provider-specific, unchanged)` |
| `compensation.lockIns[].stateDate` | `extensions (provider-specific, unchanged)` |
| `compensation.lockIns[].authUser` | `extensions (provider-specific, unchanged)` |
| `compensation.formI9Filed` | `extensions (provider-specific, unchanged)` |
| `compensation.formI9RenewDate` | `extensions (provider-specific, unchanged)` |
| `compensation.notes` | `extensions (provider-specific, unchanged)` |
| `compensation.ficaExempt` | `extensions (provider-specific, unchanged)` |
| `compensation.benefitsPerHour` | `extensions (provider-specific, unchanged)` |
| `compensation.perfAgreement` | `extensions (provider-specific, unchanged)` |
| `compensation.payRate2` | `extensions (provider-specific, unchanged)` |
| `compensation.payRate3` | `extensions (provider-specific, unchanged)` |
| `compensation.payRate4` | `extensions (provider-specific, unchanged)` |
| `compensation.payChangeLastDate` | `extensions (provider-specific, unchanged)` |
| `compensation.overrideWorkGeocode` | `extensions (provider-specific, unchanged)` |
| `compensation.familyMemberMI` | `extensions (provider-specific, unchanged)` |
| `compensation.probationCodeMO` | `extensions (provider-specific, unchanged)` |
| `compensation.electronicPayStub` | `extensions (provider-specific, unchanged)` |
| `compensation.healthInsVT` | `extensions (provider-specific, unchanged)` |
| `compensation.lastWorkedDate` | `extensions (provider-specific, unchanged)` |
| `compensation.irsLockInDate` | `extensions (provider-specific, unchanged)` |
| `compensation.nonResAlien` | `extensions (provider-specific, unchanged)` |
| `compensation.alienRegExpDate` | `extensions (provider-specific, unchanged)` |
| `compensation.benefitSalary` | `extensions (provider-specific, unchanged)` |
| `compensation.citizenshipStatus` | `extensions (provider-specific, unchanged)` |
| `compensation.firstPayPeriodHours` | `extensions (provider-specific, unchanged)` |
| `compensation.compensationChecksum` | `extensions (provider-specific, unchanged)` |
| `compensation.providerNotifiedOn` | `extensions (provider-specific, unchanged)` |
| `compensation.alternateId` | `extensions (provider-specific, unchanged)` |
| `compensation.w8Filed` | `extensions (provider-specific, unchanged)` |
| `directDeposit.achStatus` | `data.deposit_settings.achStatus` |
| `directDeposit.voucherType` | `data.deposit_settings.voucherType` |
| `directDeposit.suppressAccountPrint` | `data.deposit_settings.suppressAccountPrint` |
| `directDeposit.achVoucher[].transitNum` | `data.deposit_settings.achVoucher[].transitNum` |
| `directDeposit.achVoucher[].accountNum` | `data.deposit_settings.achVoucher[].accountNum` |
| `directDeposit.achVoucher[].accountType` | `data.deposit_settings.achVoucher[].accountType` |
| `directDeposit.achVoucher[].method` | `data.deposit_settings.achVoucher[].method` |
| `directDeposit.achVoucher[].amount` | `data.deposit_settings.achVoucher[].amount` |
| `directDeposit.achVoucher[].limit` | `data.deposit_settings.achVoucher[].limit` |
| `directDeposit.achVoucher[].status` | `data.deposit_settings.achVoucher[].status` |
| `directDeposit.achVoucher[].bankName` | `data.deposit_settings.achVoucher[].bankName` |
| `directDeposit.achVoucher[].voucherTypeOverride` | `data.deposit_settings.achVoucher[].voucherTypeOverride` |
| `directDeposit.directDepositChecksum` | `data.deposit_settings.directDepositChecksum` |
| `hsa.hsaDepositSettings[].transitNum` | `data.hsa.hsaDepositSettings[].transitNum` |
| `hsa.hsaDepositSettings[].accountNum` | `data.hsa.hsaDepositSettings[].accountNum` |
| `hsa.hsaDepositSettings[].accountType` | `data.hsa.hsaDepositSettings[].accountType` |
| `hsa.hsaDepositSettings[].method` | `data.hsa.hsaDepositSettings[].method` |
| `hsa.hsaDepositSettings[].amount` | `data.hsa.hsaDepositSettings[].amount` |
| `hsa.hsaDepositSettings[].status` | `data.hsa.hsaDepositSettings[].status` |
| `hsa.hsaDepositSettings[].bankName` | `data.hsa.hsaDepositSettings[].bankName` |
| `hsa.hsaDepositSettings[].voucherTypeOverride` | `data.hsa.hsaDepositSettings[].voucherTypeOverride` |
| `hsa.achChecksum` | `data.hsa.achChecksum` |
| `employeeEvents.employeeEvent[].eventCode` | `extensions (provider-specific, unchanged)` |
| `employeeEvents.employeeEvent[].effectiveDate` | `extensions (provider-specific, unchanged)` |
| `employeeEvents.employeeEvent[].description` | `extensions (provider-specific, unchanged)` |
| `employeeEvents.employeeEvent[].actionDate` | `extensions (provider-specific, unchanged)` |
| `employeeEvents.employeeEvent[].comment` | `extensions (provider-specific, unchanged)` |
| `health.allergy[]` | `data.health.allergy[]` |
| `health.condition[]` | `data.health.condition[]` |
| `health.program[]` | `data.health.program[]` |
| `health.height` | `data.health.height` |
| `health.weight` | `data.health.weight` |
| `health.bloodType` | `data.health.bloodType` |
| `health.bloodRh` | `data.health.bloodRh` |
| `health.bloodDonor` | `data.health.bloodDonor` |
| `health.donateDateLast` | `data.health.donateDateLast` |
| `health.donateDateNext` | `data.health.donateDateNext` |
| `health.drugTestResult` | `data.health.drugTestResult` |
| `health.drugTestDateLast` | `data.health.drugTestDateLast` |
| `health.drugTestDateNext` | `data.health.drugTestDateNext` |
| `health.audioTestResult` | `data.health.audioTestResult` |
| `health.audioTestDateLast` | `data.health.audioTestDateLast` |
| `health.audioTestDateNext` | `data.health.audioTestDateNext` |
| `health.physExamResult` | `data.health.physExamResult` |
| `health.physExamDateLast` | `data.health.physExamDateLast` |
| `health.physExamDateNext` | `data.health.physExamDateNext` |
| `skillsAndEducation.skillChecksum` | `data.skills_education.skillChecksum` |
| `skillsAndEducation.skill[].skillCode` | `data.skills_education.skill[].skillCode` |
| `skillsAndEducation.skill[].competencyLevel` | `data.skills_education.skill[].competencyLevel` |
| `skillsAndEducation.skill[].certifyDate` | `data.skills_education.skill[].certifyDate` |
| `skillsAndEducation.skill[].skillComment` | `data.skills_education.skill[].skillComment` |
| `skillsAndEducation.skill[].renewDate` | `data.skills_education.skill[].renewDate` |
| `skillsAndEducation.school[].schoolName` | `data.skills_education.school[].schoolName` |
| `skillsAndEducation.school[].schoolYear` | `data.skills_education.school[].schoolYear` |
| `skillsAndEducation.school[].graduated` | `data.skills_education.school[].graduated` |
| `skillsAndEducation.school[].gradYear` | `data.skills_education.school[].gradYear` |
| `skillsAndEducation.school[].degreeEarned` | `data.skills_education.school[].degreeEarned` |
| `skillsAndEducation.school[].schoolComment` | `data.skills_education.school[].schoolComment` |
| `skillsAndEducation.osha10Certified` | `data.skills_education.osha10Certified` |
| `absenceJournalId[]` | `extensions (provider-specific, unchanged)` |
| `benefitEnrollmentCompleted` | `extensions (provider-specific, unchanged)` |
| `scheduledDeduction[].deductionCode` | `data.scheduled_deductions[].deductionCode` |
| `scheduledDeduction[].checkStubDescription` | `data.scheduled_deductions[].checkStubDescription` |
| `scheduledDeduction[].status` | `data.scheduled_deductions[].status` |
| `scheduledDeduction[].amount` | `data.scheduled_deductions[].amount` |
| `scheduledDeduction[].startDate` | `data.scheduled_deductions[].startDate` |
| `scheduledDeduction[].stopDate` | `data.scheduled_deductions[].stopDate` |
| `scheduledDeduction[].cutbackPayeeCode` | `data.scheduled_deductions[].cutbackPayeeCode` |
| `newHireQuestions[].code` | `extensions (provider-specific, unchanged)` |
| `newHireQuestions[].description` | `extensions (provider-specific, unchanged)` |
| `newHireQuestions[].answer` | `extensions (provider-specific, unchanged)` |
| `enrollmentInProgress.enrollmentInProgress` | `extensions (provider-specific, unchanged)` |
| `enrollmentInProgress.enrollmentType` | `extensions (provider-specific, unchanged)` |

## isolved

Source: `contracts/isolved/openapi/isolved-v6.swagger.json#/definitions/AOS.PayrollOffice.RestAPI.Models.EmployeeModel`

| Source path | Destination / treatment |
| --- | --- |
| `id` | `data.source_id + scoped identity` |
| `acaEmploymentStatus` | `extensions (provider-specific, unchanged)` |
| `activeDutySeparationDate` | `extensions (provider-specific, unchanged)` |
| `adjustedServiceDate` | `extensions (provider-specific, unchanged)` |
| `annualSalary` | `data.compensation.annual_salary` |
| `assignedManager.id` | `extensions (provider-specific, unchanged)` |
| `assignedManager.employeeName` | `extensions (provider-specific, unchanged)` |
| `assignedManager.employeeNumber` | `extensions (provider-specific, unchanged)` |
| `assignedManager.jobTitle` | `extensions (provider-specific, unchanged)` |
| `assignedManager.legalId` | `extensions (provider-specific, unchanged)` |
| `assignedManager.payrollEmploymentStatusCode` | `extensions (provider-specific, unchanged)` |
| `assignedManager.links[].href` | `extensions (provider-specific, unchanged)` |
| `assignedManager.links[].method` | `extensions (provider-specific, unchanged)` |
| `assignedManager.links[].rel` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.id` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.employeeName` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.employeeNumber` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.jobTitle` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.legalId` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.payrollEmploymentStatusCode` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.links[].href` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.links[].method` | `extensions (provider-specific, unchanged)` |
| `assignedSupervisor.links[].rel` | `extensions (provider-specific, unchanged)` |
| `attachments[].id` | `extensions (provider-specific, unchanged)` |
| `attachments[].allowEmployeeAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].allowManagerAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].allowSupervisorAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].clientMessageAttachmentId` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentCategory` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentContent` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentDescription` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentFileName` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentMimeType` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentType` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentTypeDescription` | `extensions (provider-specific, unchanged)` |
| `attachments[].documentUploadDate` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.id` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.fileCategory.id` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.fileCategory.documentCategoryDescription` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.fileCategory.links[].href` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.fileCategory.links[].method` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.fileCategory.links[].rel` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.subcategoryDescription` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.links[].href` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.links[].method` | `extensions (provider-specific, unchanged)` |
| `attachments[].fileSubCategory.links[].rel` | `extensions (provider-specific, unchanged)` |
| `attachments[].isSystemGenerated` | `extensions (provider-specific, unchanged)` |
| `attachments[].readonlyEmployeeAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].readonlyManagerAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].readonlySupervisorAccess` | `extensions (provider-specific, unchanged)` |
| `attachments[].requiresElectronicSignature` | `extensions (provider-specific, unchanged)` |
| `attachments[].signedAcknowledgementDocumentType` | `extensions (provider-specific, unchanged)` |
| `attachments[].systemMessageAttachmentId` | `extensions (provider-specific, unchanged)` |
| `attachments[].links[].href` | `extensions (provider-specific, unchanged)` |
| `attachments[].links[].method` | `extensions (provider-specific, unchanged)` |
| `attachments[].links[].rel` | `extensions (provider-specific, unchanged)` |
| `birthDate` | `data.profile.birth_date` |
| `citizenship` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].id` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].accountNumber` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].accountType` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].amount` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].bankName` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].description` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].frequency` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].percent` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].routingNumber` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].sequenceNumber` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].status` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].links[].href` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].links[].method` | `extensions (provider-specific, unchanged)` |
| `directDeposits[].links[].rel` | `extensions (provider-specific, unchanged)` |
| `disabilityDescription` | `extensions (provider-specific, unchanged)` |
| `disabilityNotes` | `extensions (provider-specific, unchanged)` |
| `disabled` | `data.profile.disabled` |
| `disabledEffectiveDate` | `data.profile.disability_effective_date` |
| `disabledRequiresAccomodation` | `extensions (provider-specific, unchanged)` |
| `eeoGenderOverride` | `extensions (provider-specific, unchanged)` |
| `eligibleForRehire` | `data.employment.eligible_for_rehire` |
| `emailAddress` | `data.contact.email` |
| `employeeNumber` | `data.employment.employee_number` |
| `employmentCategoryCode` | `data.employment.type_code` |
| `employmentCategoryEffectiveDate` | `data.employment.category_effective_date` |
| `employmentCategoryFullTimeEquivalent` | `data.employment.fte` |
| `employmentStatus` | `data.employment.status (tenant lookup)` |
| `enableSelfService` | `extensions (provider-specific, unchanged)` |
| `ethnicOrigin` | `data.profile.ethnicity_code` |
| `gender` | `data.profile.gender_code` |
| `hireDate` | `data.employment.hire_date` |
| `hourlyRate` | `data.compensation.hourly_rate` |
| `i9Documents.documentA.allowEmployeeAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.allowManagerAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.allowSupervisorAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.documentCode` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.documentContent` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.documentDescription` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.documentFileName` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.documentNumber` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.expirationDate` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.issuingAuthority` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.links[].href` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.links[].method` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentA.links[].rel` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.allowEmployeeAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.allowManagerAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.allowSupervisorAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.documentCode` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.documentContent` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.documentDescription` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.documentFileName` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.documentNumber` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.expirationDate` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.issuingAuthority` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.links[].href` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.links[].method` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentB.links[].rel` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.allowEmployeeAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.allowManagerAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.allowSupervisorAccess` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.documentCode` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.documentContent` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.documentDescription` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.documentFileName` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.documentNumber` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.expirationDate` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.issuingAuthority` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.links[].href` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.links[].method` | `extensions (provider-specific, unchanged)` |
| `i9Documents.documentC.links[].rel` | `extensions (provider-specific, unchanged)` |
| `i9Documents.i9Completed` | `extensions (provider-specific, unchanged)` |
| `i9Documents.i9CompletedDate` | `extensions (provider-specific, unchanged)` |
| `idType` | `extensions (provider-specific, unchanged)` |
| `isManager` | `extensions (provider-specific, unchanged)` |
| `isPending` | `data.employment.pending` |
| `isRecentlySeparatedVeteran` | `extensions (provider-specific, unchanged)` |
| `isRemoteWorker` | `data.employment.remote_worker` |
| `isSupervisor` | `extensions (provider-specific, unchanged)` |
| `jobCode` | `data.job.code` |
| `jobEeoCategory` | `data.job.eeo_category_code` |
| `jobEffectiveDate` | `data.job.start_date` |
| `jobFLSAExempt` | `data.job.flsa_exempt` |
| `jobGroup` | `data.job.group` |
| `jobId` | `extensions (provider-specific, unchanged)` |
| `jobIsSeasonal` | `data.job.seasonal` |
| `jobIsUnion` | `data.job.union` |
| `jobTitle` | `data.job.title` |
| `labors[].laborDescription` | `data.organization.labor_assignments[].laborDescription` |
| `labors[].laborField` | `data.organization.labor_assignments[].laborField` |
| `labors[].laborFieldId` | `data.organization.labor_assignments[].laborFieldId` |
| `labors[].laborValue` | `data.organization.labor_assignments[].laborValue` |
| `legalCode` | `extensions (provider-specific, unchanged)` |
| `maritalStatus` | `data.profile.marital_status_code` |
| `messages[].id` | `extensions (provider-specific, unchanged)` |
| `messages[].description` | `extensions (provider-specific, unchanged)` |
| `messages[].links[].href` | `extensions (provider-specific, unchanged)` |
| `messages[].links[].method` | `extensions (provider-specific, unchanged)` |
| `messages[].links[].rel` | `extensions (provider-specific, unchanged)` |
| `militaryStatus` | `data.profile.military_status_code` |
| `miscDataSets[].fields[].id.category` | `data.custom_data_sets[].fields[].id.category` |
| `miscDataSets[].fields[].id.dataType` | `data.custom_data_sets[].fields[].id.dataType` |
| `miscDataSets[].fields[].id.fieldCode` | `data.custom_data_sets[].fields[].id.fieldCode` |
| `miscDataSets[].fields[].id.fieldTitle` | `data.custom_data_sets[].fields[].id.fieldTitle` |
| `miscDataSets[].fields[].id.lookups[].description` | `data.custom_data_sets[].fields[].id.lookups[].description` |
| `miscDataSets[].fields[].id.lookups[].id` | `data.custom_data_sets[].fields[].id.lookups[].id` |
| `miscDataSets[].fields[].miscValue` | `data.custom_data_sets[].fields[].miscValue` |
| `miscDataSets[].id` | `data.custom_data_sets[].id` |
| `miscDataSets[].isDeleted` | `data.custom_data_sets[].isDeleted` |
| `miscDataSets[].miscFieldCategory.categoryTitle` | `data.custom_data_sets[].miscFieldCategory.categoryTitle` |
| `miscDataSets[].miscFieldCategory.id` | `data.custom_data_sets[].miscFieldCategory.id` |
| `miscDataSets[].miscFieldCategory.isDataSet` | `data.custom_data_sets[].miscFieldCategory.isDataSet` |
| `miscFields[].title` | `data.custom_fields[].title` |
| `miscFields[].value` | `data.custom_fields[].value` |
| `nameAddress.id` | `extensions (provider-specific, unchanged)` |
| `nameAddress.address1` | `data.address.line1` |
| `nameAddress.address2` | `data.address.line2` |
| `nameAddress.city` | `data.address.city` |
| `nameAddress.firstName` | `data.profile.first_name` |
| `nameAddress.lastName` | `data.profile.last_name` |
| `nameAddress.middleName` | `data.profile.middle_name` |
| `nameAddress.overrideAddress.address1` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.address2` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.city` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.country` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.deleteAddress` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.foreignPostalCode` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.foreignStateProvince` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.militaryCity` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.militaryState` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.state` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.useForPaychecks` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.useForTaxForms` | `extensions (provider-specific, unchanged)` |
| `nameAddress.overrideAddress.zipCode` | `extensions (provider-specific, unchanged)` |
| `nameAddress.preferredName` | `data.profile.preferred_name` |
| `nameAddress.preferredPronouns` | `data.profile.pronouns` |
| `nameAddress.prefix` | `extensions (provider-specific, unchanged)` |
| `nameAddress.residentGeoCode` | `extensions (provider-specific, unchanged)` |
| `nameAddress.schoolDistrictCode` | `extensions (provider-specific, unchanged)` |
| `nameAddress.state` | `data.address.region` |
| `nameAddress.suffix` | `extensions (provider-specific, unchanged)` |
| `nameAddress.zipCode` | `data.address.postal_code` |
| `nameAddress.links[].href` | `extensions (provider-specific, unchanged)` |
| `nameAddress.links[].method` | `extensions (provider-specific, unchanged)` |
| `nameAddress.links[].rel` | `extensions (provider-specific, unchanged)` |
| `normalHours` | `data.compensation.standard_hours` |
| `organizations[].id` | `data.organization.assignments[].id` |
| `organizations[].displayOrder` | `data.organization.assignments[].displayOrder` |
| `organizations[].organizationId` | `data.organization.assignments[].organizationId` |
| `organizations[].title` | `data.organization.assignments[].title` |
| `organizations[].value` | `data.organization.assignments[].value` |
| `organizations[].valueDescription` | `data.organization.assignments[].valueDescription` |
| `originalHireDate` | `data.employment.first_hire_date` |
| `overrideAddress.address1` | `data.tax_address_override.address1` |
| `overrideAddress.address2` | `data.tax_address_override.address2` |
| `overrideAddress.city` | `data.tax_address_override.city` |
| `overrideAddress.country` | `data.tax_address_override.country` |
| `overrideAddress.deleteAddress` | `data.tax_address_override.deleteAddress` |
| `overrideAddress.foreignPostalCode` | `data.tax_address_override.foreignPostalCode` |
| `overrideAddress.foreignStateProvince` | `data.tax_address_override.foreignStateProvince` |
| `overrideAddress.militaryCity` | `data.tax_address_override.militaryCity` |
| `overrideAddress.militaryState` | `data.tax_address_override.militaryState` |
| `overrideAddress.state` | `data.tax_address_override.state` |
| `overrideAddress.useForPaychecks` | `data.tax_address_override.useForPaychecks` |
| `overrideAddress.useForTaxForms` | `data.tax_address_override.useForTaxForms` |
| `overrideAddress.zipCode` | `data.tax_address_override.zipCode` |
| `payFrequency` | `data.compensation.periods_per_year` |
| `payGroup` | `data.compensation.pay_group` |
| `payRates[].payRateName` | `data.compensation.alternate_rates[].payRateName` |
| `payRates[].rateValue` | `data.compensation.alternate_rates[].rateValue` |
| `payType` | `extensions (provider-specific, unchanged)` |
| `perPaySalary` | `data.compensation.period_salary` |
| `personal.id` | `extensions (provider-specific, unchanged)` |
| `personal.faxNumber` | `data.contact.fax` |
| `personal.homePhone` | `data.contact.home_phone` |
| `personal.mobilePhone` | `data.contact.mobile_phone` |
| `personal.officePhone` | `data.contact.work_phone` |
| `personal.personalEmailAddress` | `data.contact.personal_email` |
| `personal.preferredPronouns` | `extensions (provider-specific, unchanged)` |
| `personal.links[].href` | `extensions (provider-specific, unchanged)` |
| `personal.links[].method` | `extensions (provider-specific, unchanged)` |
| `personal.links[].rel` | `extensions (provider-specific, unchanged)` |
| `previousPunchLabors[].id` | `extensions (provider-specific, unchanged)` |
| `previousPunchLabors[].description` | `extensions (provider-specific, unchanged)` |
| `previousPunchLabors[].links[].href` | `extensions (provider-specific, unchanged)` |
| `previousPunchLabors[].links[].method` | `extensions (provider-specific, unchanged)` |
| `previousPunchLabors[].links[].rel` | `extensions (provider-specific, unchanged)` |
| `profilePicture` | `extensions (provider-specific, unchanged)` |
| `protectedVeteran` | `data.profile.protected_veteran` |
| `reciprocityRule` | `extensions (provider-specific, unchanged)` |
| `rehireDate` | `data.employment.rehire_date` |
| `salaryEffectiveDate` | `data.compensation.effective_date` |
| `socCode` | `data.job.soc_code` |
| `ssn` | `extensions (provider-specific, unchanged)` |
| `statusDate` | `data.employment.status_date` |
| `taxes.federal.id` | `data.tax_settings.federal.id` |
| `taxes.federal.additionalAmount` | `data.tax_settings.federal.additionalAmount` |
| `taxes.federal.additionalIncomeAmount` | `data.tax_settings.federal.additionalIncomeAmount` |
| `taxes.federal.additionalPercent` | `data.tax_settings.federal.additionalPercent` |
| `taxes.federal.alternateCalculation` | `data.tax_settings.federal.alternateCalculation` |
| `taxes.federal.deductionExemptionAmount` | `data.tax_settings.federal.deductionExemptionAmount` |
| `taxes.federal.dependantExemptionAmount` | `data.tax_settings.federal.dependantExemptionAmount` |
| `taxes.federal.exemptionAmount` | `data.tax_settings.federal.exemptionAmount` |
| `taxes.federal.filingStatus` | `data.tax_settings.federal.filingStatus` |
| `taxes.federal.isBlocked` | `data.tax_settings.federal.isBlocked` |
| `taxes.federal.multipleJobsOrSpouseWorks` | `data.tax_settings.federal.multipleJobsOrSpouseWorks` |
| `taxes.federal.primaryExemptions` | `data.tax_settings.federal.primaryExemptions` |
| `taxes.federal.secondaryExemptions` | `data.tax_settings.federal.secondaryExemptions` |
| `taxes.federal.taxCategoryId` | `data.tax_settings.federal.taxCategoryId` |
| `taxes.federal.taxDescription` | `data.tax_settings.federal.taxDescription` |
| `taxes.federal.taxState` | `data.tax_settings.federal.taxState` |
| `taxes.federal.links[].href` | `data.tax_settings.federal.links[].href` |
| `taxes.federal.links[].method` | `data.tax_settings.federal.links[].method` |
| `taxes.federal.links[].rel` | `data.tax_settings.federal.links[].rel` |
| `taxes.nonResidentCity.id` | `data.tax_settings.nonResidentCity.id` |
| `taxes.nonResidentCity.additionalAmount` | `data.tax_settings.nonResidentCity.additionalAmount` |
| `taxes.nonResidentCity.additionalIncomeAmount` | `data.tax_settings.nonResidentCity.additionalIncomeAmount` |
| `taxes.nonResidentCity.additionalPercent` | `data.tax_settings.nonResidentCity.additionalPercent` |
| `taxes.nonResidentCity.alternateCalculation` | `data.tax_settings.nonResidentCity.alternateCalculation` |
| `taxes.nonResidentCity.deductionExemptionAmount` | `data.tax_settings.nonResidentCity.deductionExemptionAmount` |
| `taxes.nonResidentCity.dependantExemptionAmount` | `data.tax_settings.nonResidentCity.dependantExemptionAmount` |
| `taxes.nonResidentCity.exemptionAmount` | `data.tax_settings.nonResidentCity.exemptionAmount` |
| `taxes.nonResidentCity.filingStatus` | `data.tax_settings.nonResidentCity.filingStatus` |
| `taxes.nonResidentCity.isBlocked` | `data.tax_settings.nonResidentCity.isBlocked` |
| `taxes.nonResidentCity.multipleJobsOrSpouseWorks` | `data.tax_settings.nonResidentCity.multipleJobsOrSpouseWorks` |
| `taxes.nonResidentCity.primaryExemptions` | `data.tax_settings.nonResidentCity.primaryExemptions` |
| `taxes.nonResidentCity.secondaryExemptions` | `data.tax_settings.nonResidentCity.secondaryExemptions` |
| `taxes.nonResidentCity.taxCategoryId` | `data.tax_settings.nonResidentCity.taxCategoryId` |
| `taxes.nonResidentCity.taxDescription` | `data.tax_settings.nonResidentCity.taxDescription` |
| `taxes.nonResidentCity.taxState` | `data.tax_settings.nonResidentCity.taxState` |
| `taxes.nonResidentCity.links[].href` | `data.tax_settings.nonResidentCity.links[].href` |
| `taxes.nonResidentCity.links[].method` | `data.tax_settings.nonResidentCity.links[].method` |
| `taxes.nonResidentCity.links[].rel` | `data.tax_settings.nonResidentCity.links[].rel` |
| `taxes.nonResidentState.id` | `data.tax_settings.nonResidentState.id` |
| `taxes.nonResidentState.additionalAmount` | `data.tax_settings.nonResidentState.additionalAmount` |
| `taxes.nonResidentState.additionalIncomeAmount` | `data.tax_settings.nonResidentState.additionalIncomeAmount` |
| `taxes.nonResidentState.additionalPercent` | `data.tax_settings.nonResidentState.additionalPercent` |
| `taxes.nonResidentState.alternateCalculation` | `data.tax_settings.nonResidentState.alternateCalculation` |
| `taxes.nonResidentState.deductionExemptionAmount` | `data.tax_settings.nonResidentState.deductionExemptionAmount` |
| `taxes.nonResidentState.dependantExemptionAmount` | `data.tax_settings.nonResidentState.dependantExemptionAmount` |
| `taxes.nonResidentState.exemptionAmount` | `data.tax_settings.nonResidentState.exemptionAmount` |
| `taxes.nonResidentState.filingStatus` | `data.tax_settings.nonResidentState.filingStatus` |
| `taxes.nonResidentState.isBlocked` | `data.tax_settings.nonResidentState.isBlocked` |
| `taxes.nonResidentState.multipleJobsOrSpouseWorks` | `data.tax_settings.nonResidentState.multipleJobsOrSpouseWorks` |
| `taxes.nonResidentState.primaryExemptions` | `data.tax_settings.nonResidentState.primaryExemptions` |
| `taxes.nonResidentState.secondaryExemptions` | `data.tax_settings.nonResidentState.secondaryExemptions` |
| `taxes.nonResidentState.taxCategoryId` | `data.tax_settings.nonResidentState.taxCategoryId` |
| `taxes.nonResidentState.taxDescription` | `data.tax_settings.nonResidentState.taxDescription` |
| `taxes.nonResidentState.taxState` | `data.tax_settings.nonResidentState.taxState` |
| `taxes.nonResidentState.links[].href` | `data.tax_settings.nonResidentState.links[].href` |
| `taxes.nonResidentState.links[].method` | `data.tax_settings.nonResidentState.links[].method` |
| `taxes.nonResidentState.links[].rel` | `data.tax_settings.nonResidentState.links[].rel` |
| `taxes.residentCity.id` | `data.tax_settings.residentCity.id` |
| `taxes.residentCity.additionalAmount` | `data.tax_settings.residentCity.additionalAmount` |
| `taxes.residentCity.additionalIncomeAmount` | `data.tax_settings.residentCity.additionalIncomeAmount` |
| `taxes.residentCity.additionalPercent` | `data.tax_settings.residentCity.additionalPercent` |
| `taxes.residentCity.alternateCalculation` | `data.tax_settings.residentCity.alternateCalculation` |
| `taxes.residentCity.deductionExemptionAmount` | `data.tax_settings.residentCity.deductionExemptionAmount` |
| `taxes.residentCity.dependantExemptionAmount` | `data.tax_settings.residentCity.dependantExemptionAmount` |
| `taxes.residentCity.exemptionAmount` | `data.tax_settings.residentCity.exemptionAmount` |
| `taxes.residentCity.filingStatus` | `data.tax_settings.residentCity.filingStatus` |
| `taxes.residentCity.isBlocked` | `data.tax_settings.residentCity.isBlocked` |
| `taxes.residentCity.multipleJobsOrSpouseWorks` | `data.tax_settings.residentCity.multipleJobsOrSpouseWorks` |
| `taxes.residentCity.primaryExemptions` | `data.tax_settings.residentCity.primaryExemptions` |
| `taxes.residentCity.secondaryExemptions` | `data.tax_settings.residentCity.secondaryExemptions` |
| `taxes.residentCity.taxCategoryId` | `data.tax_settings.residentCity.taxCategoryId` |
| `taxes.residentCity.taxDescription` | `data.tax_settings.residentCity.taxDescription` |
| `taxes.residentCity.taxState` | `data.tax_settings.residentCity.taxState` |
| `taxes.residentCity.links[].href` | `data.tax_settings.residentCity.links[].href` |
| `taxes.residentCity.links[].method` | `data.tax_settings.residentCity.links[].method` |
| `taxes.residentCity.links[].rel` | `data.tax_settings.residentCity.links[].rel` |
| `taxes.residentState.id` | `data.tax_settings.residentState.id` |
| `taxes.residentState.additionalAmount` | `data.tax_settings.residentState.additionalAmount` |
| `taxes.residentState.additionalIncomeAmount` | `data.tax_settings.residentState.additionalIncomeAmount` |
| `taxes.residentState.additionalPercent` | `data.tax_settings.residentState.additionalPercent` |
| `taxes.residentState.alternateCalculation` | `data.tax_settings.residentState.alternateCalculation` |
| `taxes.residentState.deductionExemptionAmount` | `data.tax_settings.residentState.deductionExemptionAmount` |
| `taxes.residentState.dependantExemptionAmount` | `data.tax_settings.residentState.dependantExemptionAmount` |
| `taxes.residentState.exemptionAmount` | `data.tax_settings.residentState.exemptionAmount` |
| `taxes.residentState.filingStatus` | `data.tax_settings.residentState.filingStatus` |
| `taxes.residentState.isBlocked` | `data.tax_settings.residentState.isBlocked` |
| `taxes.residentState.multipleJobsOrSpouseWorks` | `data.tax_settings.residentState.multipleJobsOrSpouseWorks` |
| `taxes.residentState.primaryExemptions` | `data.tax_settings.residentState.primaryExemptions` |
| `taxes.residentState.secondaryExemptions` | `data.tax_settings.residentState.secondaryExemptions` |
| `taxes.residentState.taxCategoryId` | `data.tax_settings.residentState.taxCategoryId` |
| `taxes.residentState.taxDescription` | `data.tax_settings.residentState.taxDescription` |
| `taxes.residentState.taxState` | `data.tax_settings.residentState.taxState` |
| `taxes.residentState.links[].href` | `data.tax_settings.residentState.links[].href` |
| `taxes.residentState.links[].method` | `data.tax_settings.residentState.links[].method` |
| `taxes.residentState.links[].rel` | `data.tax_settings.residentState.links[].rel` |
| `taxExemptStatus` | `extensions (provider-specific, unchanged)` |
| `team.id` | `data.organization.team.id` |
| `team.calendarRule.id` | `data.organization.team.calendarRule.id` |
| `team.calendarRule.restrictedAbsencePolicies[].id` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].id` |
| `team.calendarRule.restrictedAbsencePolicies[].absenceName` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].absenceName` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.id` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.id` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.accrualDescription` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.accrualDescription` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.accrualName` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.accrualName` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.links[].href` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.links[].href` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.links[].method` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.links[].method` |
| `team.calendarRule.restrictedAbsencePolicies[].accrual.links[].rel` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].accrual.links[].rel` |
| `team.calendarRule.restrictedAbsencePolicies[].allowEmployeeAccess` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].allowEmployeeAccess` |
| `team.calendarRule.restrictedAbsencePolicies[].allowManagerAccess` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].allowManagerAccess` |
| `team.calendarRule.restrictedAbsencePolicies[].allowSupervisorAccess` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].allowSupervisorAccess` |
| `team.calendarRule.restrictedAbsencePolicies[].allowTimeOffRequest` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].allowTimeOffRequest` |
| `team.calendarRule.restrictedAbsencePolicies[].defaultHours` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].defaultHours` |
| `team.calendarRule.restrictedAbsencePolicies[].isEarningPayItem` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].isEarningPayItem` |
| `team.calendarRule.restrictedAbsencePolicies[].maximumHours` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].maximumHours` |
| `team.calendarRule.restrictedAbsencePolicies[].minimumHours` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].minimumHours` |
| `team.calendarRule.restrictedAbsencePolicies[].timeOffRequestBalanceLimit` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].timeOffRequestBalanceLimit` |
| `team.calendarRule.restrictedAbsencePolicies[].timeOffRequestDurationLimitDays` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].timeOffRequestDurationLimitDays` |
| `team.calendarRule.restrictedAbsencePolicies[].validHourValues[]` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].validHourValues[]` |
| `team.calendarRule.restrictedAbsencePolicies[].links[].href` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].links[].href` |
| `team.calendarRule.restrictedAbsencePolicies[].links[].method` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].links[].method` |
| `team.calendarRule.restrictedAbsencePolicies[].links[].rel` | `data.organization.team.calendarRule.restrictedAbsencePolicies[].links[].rel` |
| `team.calendarRule.ruleDescription` | `data.organization.team.calendarRule.ruleDescription` |
| `team.calendarRule.ruleName` | `data.organization.team.calendarRule.ruleName` |
| `team.calendarRule.timeOffRestrictionDates[].endDate` | `data.organization.team.calendarRule.timeOffRestrictionDates[].endDate` |
| `team.calendarRule.timeOffRestrictionDates[].startDate` | `data.organization.team.calendarRule.timeOffRestrictionDates[].startDate` |
| `team.calendarRule.links[].href` | `data.organization.team.calendarRule.links[].href` |
| `team.calendarRule.links[].method` | `data.organization.team.calendarRule.links[].method` |
| `team.calendarRule.links[].rel` | `data.organization.team.calendarRule.links[].rel` |
| `team.organizationField` | `data.organization.team.organizationField` |
| `team.organizationValues[].code` | `data.organization.team.organizationValues[].code` |
| `team.organizationValues[].description` | `data.organization.team.organizationValues[].description` |
| `team.organizationValues[].isInactive` | `data.organization.team.organizationValues[].isInactive` |
| `team.teamDescription` | `data.organization.team.teamDescription` |
| `team.teamName` | `data.organization.team.teamName` |
| `team.links[].href` | `data.organization.team.links[].href` |
| `team.links[].method` | `data.organization.team.links[].method` |
| `team.links[].rel` | `data.organization.team.links[].rel` |
| `terminationDate` | `data.employment.termination_date` |
| `terminationReason` | `data.employment.termination_reason_code` |
| `terminationType` | `extensions (provider-specific, unchanged)` |
| `timecardPunchStatusDate` | `extensions (provider-specific, unchanged)` |
| `timecardPunchStatusIsIn` | `extensions (provider-specific, unchanged)` |
| `timeclockId` | `extensions (provider-specific, unchanged)` |
| `tobaccoUse` | `data.profile.tobacco_use` |
| `tobaccoUseEffectiveDate` | `extensions (provider-specific, unchanged)` |
| `uniqueId` | `extensions (provider-specific, unchanged)` |
| `updatedDisabledEffectiveDate` | `extensions (provider-specific, unchanged)` |
| `updatedHireDate` | `extensions (provider-specific, unchanged)` |
| `updatedJobEffectiveDate` | `extensions (provider-specific, unchanged)` |
| `updatedSalaryEffectiveDate` | `extensions (provider-specific, unchanged)` |
| `updatedStatusDate` | `extensions (provider-specific, unchanged)` |
| `veteranStatusNotSpecified` | `extensions (provider-specific, unchanged)` |
| `workersCompCode` | `data.employment.workers_comp_code` |
| `workLocation` | `data.organization.location_code` |
| `workLocationDashDescription` | `extensions (provider-specific, unchanged)` |
| `wotc.applicationDate` | `extensions (provider-specific, unchanged)` |
| `wotc.includeCertification` | `extensions (provider-specific, unchanged)` |
| `wotc.jobAcceptedDate` | `extensions (provider-specific, unchanged)` |
| `wotc.jobOfferedDate` | `extensions (provider-specific, unchanged)` |
| `links[].href` | `extensions (provider-specific, unchanged)` |
| `links[].method` | `extensions (provider-specific, unchanged)` |
| `links[].rel` | `extensions (provider-specific, unchanged)` |

## ukg-ready

Source: `contracts/ukg-ready/reference-schemas.json#/schemas/106/schema (reference-docs/res/__v2__companies__(cid)__employees__(aid).html#schema-0)`

| Source path | Destination / treatment |
| --- | --- |
| `id` | `data.source_id + scoped identity` |
| `username` | `extensions (provider-specific, unchanged)` |
| `first_name` | `data.profile.first_name` |
| `last_name` | `data.profile.last_name` |
| `photo_href` | `extensions (provider-specific, unchanged)` |
| `isPhotoUploaded` | `extensions (provider-specific, unchanged)` |
| `middle_name` | `data.profile.middle_name` |
| `external_id` | `extensions (provider-specific, unchanged)` |
| `employee_id` | `data.employment.employee_number` |
| `status` | `data.employment.status (tenant lookup)` |
| `bsn` | `extensions (provider-specific, unchanged)` |
| `address.country` | `data.address.country` |
| `address.address_line_1` | `data.address.line1` |
| `address.address_line_2` | `data.address.line2` |
| `address.address_line_3` | `data.address.line3` |
| `address.city` | `data.address.city` |
| `address.state` | `data.address.region` |
| `address.state_code` | `extensions (provider-specific, unchanged)` |
| `address.zip` | `data.address.postal_code` |
| `address.number` | `extensions (provider-specific, unchanged)` |
| `address.number_addition` | `extensions (provider-specific, unchanged)` |
| `use_separate_mailing_address` | `extensions (provider-specific, unchanged)` |
| `mailing_address.country` | `data.mailing_address.country` |
| `mailing_address.address_line_1` | `data.mailing_address.line1` |
| `mailing_address.address_line_2` | `data.mailing_address.line2` |
| `mailing_address.address_line_3` | `extensions (provider-specific, unchanged)` |
| `mailing_address.city` | `data.mailing_address.city` |
| `mailing_address.state` | `data.mailing_address.region` |
| `mailing_address.state_code` | `extensions (provider-specific, unchanged)` |
| `mailing_address.zip` | `data.mailing_address.postal_code` |
| `mailing_address.number` | `extensions (provider-specific, unchanged)` |
| `mailing_address.number_addition` | `extensions (provider-specific, unchanged)` |
| `primary_account_id` | `extensions (provider-specific, unchanged)` |
| `ein.id` | `data.organization.ein.id` |
| `force_change_password` | `extensions (provider-specific, unchanged)` |
| `locked` | `extensions (provider-specific, unchanged)` |
| `first_screen.id` | `extensions (provider-specific, unchanged)` |
| `phones.cell_phone_country_id` | `extensions (provider-specific, unchanged)` |
| `phones.cell_phone_country_code` | `extensions (provider-specific, unchanged)` |
| `phones.cell_phone` | `data.contact.mobile_phone` |
| `phones.home_phone_country_id` | `extensions (provider-specific, unchanged)` |
| `phones.home_phone_country_code` | `extensions (provider-specific, unchanged)` |
| `phones.home_phone` | `data.contact.home_phone` |
| `phones.work_phone_country_id` | `extensions (provider-specific, unchanged)` |
| `phones.work_phone_country_code` | `extensions (provider-specific, unchanged)` |
| `phones.work_phone` | `data.contact.work_phone` |
| `phones.preferred_phone` | `data.contact.preferred_phone_code` |
| `locale.id` | `extensions (provider-specific, unchanged)` |
| `managers[].index` | `data.organization.managers[].index` |
| `managers[].empl_ref.account_id` | `data.organization.managers[].empl_ref.account_id` |
| `national_insurance` | `extensions (provider-specific, unchanged)` |
| `nickname` | `data.profile.preferred_name` |
| `primary_email` | `data.contact.email` |
| `secondary_email` | `data.contact.secondary_email` |
| `salutation` | `data.profile.prefix` |
| `social_insurance` | `extensions (provider-specific, unchanged)` |
| `social_security` | `extensions (provider-specific, unchanged)` |
| `suffix` | `data.profile.suffix` |
| `timezone` | `data.profile.timezone` |
| `cost_centers_info.defaults[].index` | `data.organization.cost_centers.defaults[].index` |
| `cost_centers_info.defaults[].value.id` | `data.organization.cost_centers.defaults[].value.id` |
| `cost_centers_info.limits[].index` | `data.organization.cost_centers.limits[].index` |
| `cost_centers_info.limits[].values[].id` | `data.organization.cost_centers.limits[].values[].id` |
| `cost_centers_info.limits[].values[].effective_from` | `data.organization.cost_centers.limits[].values[].effective_from` |
| `cost_centers_info.limits[].values[].type` | `data.organization.cost_centers.limits[].values[].type` |
| `add_to_new_hire_export` | `extensions (provider-specific, unchanged)` |
| `dates.hired` | `data.employment.hire_date` |
| `dates.deceased` | `data.profile.deceased_date` |
| `dates.re_hired` | `data.employment.rehire_date` |
| `dates.started` | `data.employment.start_date` |
| `dates.birthday` | `data.profile.birth_date` |
| `dates.review` | `extensions (provider-specific, unchanged)` |
| `dates.seniority` | `data.employment.seniority_date` |
| `dates.frozen_benefit` | `extensions (provider-specific, unchanged)` |
| `dates.benefits` | `data.employment.benefits_date` |
| `dates.retired` | `data.employment.retired_date` |
| `dates.terminated` | `data.employment.termination_date` |
| `dates.peo_hired` | `data.employment.peo_hire_date` |
| `dates.custom_dates[].index` | `data.custom_dates[].index` |
| `dates.custom_dates[].date` | `data.custom_dates[].date` |
| `account_extra_fields[].index` | `data.custom_fields[].index` |
| `account_extra_fields[].values[].value` | `data.custom_fields[].values[].value` |
| `account_extra_fields[].values[].effective_from` | `data.custom_fields[].values[].effective_from` |
| `time_entry_extra_fields[].index` | `extensions (provider-specific, unchanged)` |
| `time_entry_extra_fields[].value` | `extensions (provider-specific, unchanged)` |
| `_links.self` | `extensions (provider-specific, unchanged)` |
| `_links.demographics` | `extensions (provider-specific, unchanged)` |
| `_links.pay-info` | `extensions (provider-specific, unchanged)` |
| `_links.badges` | `extensions (provider-specific, unchanged)` |
| `_links.profiles` | `extensions (provider-specific, unchanged)` |
| `_links.hcm-profiles` | `extensions (provider-specific, unchanged)` |
| `_links.hcm-fields` | `extensions (provider-specific, unchanged)` |
| `hardware_settings.in_touch.security_level` | `extensions (provider-specific, unchanged)` |
| `hardware_settings.in_touch.pin` | `extensions (provider-specific, unchanged)` |
| `managed_cost_centers_enabled` | `extensions (provider-specific, unchanged)` |
| `managed_cost_centers_settings.allow_save_others_cost_centers` | `extensions (provider-specific, unchanged)` |
| `national_id_numbers[].type` | `data.national_identifiers[].type` |
| `national_id_numbers[].value` | `data.national_identifiers[].value` |
| `national_id_numbers[].primary` | `data.national_identifiers[].primary` |

