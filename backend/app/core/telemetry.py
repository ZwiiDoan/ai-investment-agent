import json
import os
from opentelemetry import metrics, trace
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPHTTPSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPGRPCSpanExporter,
)
from loguru import logger
from app.core.settings import settings
from starlette.responses import Response as StarletteResponse


def setup_otel(app):
    # Print all OTEL-related environment variables for debugging
    print("[DEBUG] ENVIRONMENT VARIABLES:")
    for k, v in os.environ.items():
        if "OTEL" in k:
            print(f"{k}={v}")

    # Metrics setup
    resource = Resource(attributes={"service.name": "ai-investment-agent-backend"})
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # Tracing setup
    service_name = settings.otel_service_name
    trace_resource = Resource(attributes={"service.name": service_name})
    trace.set_tracer_provider(TracerProvider(resource=trace_resource))

    otlp_protocol = os.getenv(
        "OTEL_EXPORTER_OTLP_PROTOCOL", getattr(settings, "otlp_protocol", "http")
    ).lower()

    if otlp_protocol == "grpc":
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", settings.otlp_grpc_endpoint)
        print(f"[DEBUG] OTLP gRPC exporter will POST to: {otlp_endpoint}")
        exporter = OTLPGRPCSpanExporter(
            endpoint=otlp_endpoint,
            timeout=settings.otlp_timeout_ms / 1000,
        )
        exporter_name = "OTLPGRPCSpanExporter"
    else:
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", settings.otlp_http_endpoint)
        print(f"[DEBUG] OTLP HTTP exporter will POST to: {otlp_endpoint}")
        exporter = OTLPHTTPSpanExporter(
            endpoint=otlp_endpoint,
            timeout=settings.otlp_timeout_ms / 1000,
        )
        exporter_name = "OTLPHTTPSpanExporter"
    exporter_endpoint = otlp_endpoint
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))
    FastAPIInstrumentor().instrument_app(app)

    # Log which exporter is active (one-time)
    logger.info(
        json.dumps(
            {
                "telemetry.exporter": exporter_name,
                "otel.protocol": otlp_protocol,
                "otel.endpoint": exporter_endpoint,
                "service.name": service_name,
            }
        )
    )


def metrics_endpoint():
    # OpenTelemetry Prometheus exporter exposes metrics via /metrics
    reader = metrics.get_meter_provider()._metric_readers[0]
    return StarletteResponse(reader.collect(), media_type="text/plain")
