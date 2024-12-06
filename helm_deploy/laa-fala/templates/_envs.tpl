{{/* vim: set filetype=mustache: */}}
{{/*
Environment variables for web and worker containers
*/}}
{{- define "app.envs" }}
env:
  - name: FEATURE_FLAG_SURVEY_MONKEY
    value: {{ .Values.feature_flags.survey_monkey }}
  - name: BLOCK_ROBOTS
    value: {{ .Values.feature_flags.block_robots }}
  - name: ALLOWED_HOSTS
    value: {{ .Values.allowed_hosts }}
  - name: LAALAA_API_HOST
    value: {{ .Values.laalaa_api.host }}
  - name: ENVIRONMENT
    value: {{ .Values.environment }}
  - name: FEATURE_FLAG_MAINTENANCE_MODE
    value: {{ .Values.feature_flags.maintenance_mode }}
  - name: FEATURE_FLAG_SINGLE_CATEGORY_SEARCH_FORM
    value: {{ .Values.feature_flags.single_category_search }}
{{- end }}
