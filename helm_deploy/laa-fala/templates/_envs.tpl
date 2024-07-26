{{/* vim: set filetype=mustache: */}}
{{/*
Environment variables for web and worker containers
*/}}
{{- define "app.envs" }}
env:
  {{ if .Values.postgresql.enabled }}
  - name: DB_USER
    value: {{ .Values.postgresql.auth.postgresUsername }}
  - name: DB_PASSWORD
    value: {{ .Values.postgresql.auth.postgresPassword }}
    {{/*
    This is the name of the DB service which is in service.yaml
    */}}
  - name: DB_HOST
    value: {{ include "app.fullname" . }}-db
  - name: DB_NAME
    value: {{ .Values.postgresql.auth.database }}
  {{ else }}
  - name: DB_USER
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_username
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_password
  - name: DB_HOST
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: rds_instance_address
  - name: DB_NAME
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_name
  {{ end }}
  - name: FEATURE_FLAG_SURVEY_MONKEY
    value: {{ .Values.feature_flags.survey_monkey }}
  - name: ALLOWED_HOSTS
    value: {{ .Values.allowed_hosts }}
  - name: LAALAA_API_HOST
    value: {{ .Values.laalaa_api.host }}
  - name: ENVIRONMENT
    value: {{ .Values.environment }}
{{- end }}
