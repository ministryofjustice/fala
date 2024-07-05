{{/* vim: set filetype=mustache: */}}
{{/*
Environment variables for web and worker containers
*/}}
{{- define "app.envs" }}
env:
  {{ if .Values.postgresql.enabled }}
  - name: POSTGRES_USER
    value: {{ .Values.postgresql.postgresqlUsername }}
  - name: POSTGRES_PASSWORD
    value: {{ .Values.postgresql.auth.postgresPassword }}
  - name: POSTGRES_HOST
    value: {{ printf "%s-%s" .Release.Name "postgresql" | trunc 63 | trimSuffix "-" }}
  - name: POSTGRES_DATABASE
    value: {{ .Values.postgresql.auth.database }}
  {{ else }}
  - name: POSTGRES_USER
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_username
  - name: POSTGRES_PASSWORD
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_password
  - name: POSTGRES_HOST
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: rds_instance_address
  - name: POSTGRES_DATABASE
    valueFrom:
      secretKeyRef:
        name: rds-postgresql-instance-output
        key: database_name
  {{ end }}
  - name: FEATURE_FLAG_NO_MAP
    value: {{ .Values.feature_flags.no_map }}
  - name: FEATURE_FLAG_SURVEY_MONKEY
    value: {{ .Values.feature_flags.survey_monkey }}
  - name: ALLOWED_HOSTS
    value: {{ .Values.allowed_hosts }}
  - name: GOOGLE_MAPS_API_KEY
    valueFrom:
      secretKeyRef:
        name: service-secrets
        key: GOOGLE_MAPS_API_KEY
  - name: LAALAA_API_HOST
    value: {{ .Values.laalaa_api.host }}
  - name: ENVIRONMENT
    value: {{ .Values.environment }}
{{- end }}
