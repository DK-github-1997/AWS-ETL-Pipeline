# ETL Failure Recovery Runbook

A practical checklist for investigating a failed batch pipeline. Use this as a sample runbook and adapt it to the environment before operational use.

## 1. Confirm impact
- Identify the failed job, business date, and downstream consumers.
- Check the expected completion time and SLA.
- Determine whether the load partially wrote data or failed before writing.

## 2. Review evidence
- Check scheduler status, job logs, and the first actionable error.
- Verify source file arrival, file size, schema, and record count.
- Check database connectivity, permissions, and available capacity.
- Review upstream dependencies and recent configuration changes.

## 3. Validate data before rerun
- Compare source and target row counts for the affected business date.
- Check duplicate business keys and mandatory fields.
- Confirm whether the job is idempotent and whether a partial load needs cleanup under the approved recovery procedure.
- Do not manually delete or overwrite production data without authorization.

## 4. Recover safely
- Correct the confirmed root cause.
- Rerun only the affected partition or business date when supported.
- Monitor job completion and capture the run identifier.
- Reconcile row counts and key totals after the rerun.

## 5. Close the incident
Record impact, timeline, root cause, recovery action, validation evidence, and preventive action. Escalate if the SLA is at risk or data integrity cannot be confirmed.

## Interview talking point
For a batch failure, I first assess business impact and SLA, then use logs and dependency checks to isolate the cause. Before rerunning, I confirm the load's idempotency and validate the affected data. After recovery, I reconcile source and target counts and document the RCA.
