import threading
import time
import redis
from dataclasses import dataclass
from typing import Dict
from loguru import logger
from dataclasses import field


class UserConfigNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._message = f"User {args[0]} config not found."

    def __str__(self) -> str:
        return self._message


@dataclass
class UserMetrics:
    user_id: str
    requests_count: int = 0
    blocked_count: int = 0
    last_request_time: float = 0.0
    avg_requests_per_minute: float = 0.0


@dataclass
class RateLimitMetrics:
    total_requests: int = 0
    allowed_requests: int = 0
    blocked_requests: int = 0
    redis_errors: int = 0
    avg_response_time: float = 0.0
    active_users: int = 0


@dataclass
class RedisConfig:
    host: str = field(default_factory=lambda: "localhost")
    port: int = 6379
    db: int = 0


@dataclass
class EndpointMetrics:
    endpoint: str
    total_requests: int = 0
    blocked_requests: int = 0
    unique_users: set = field(default_factory=set)


@dataclass
class UserLimitConfig:
    max_requests: int = 100
    window_seconds: int = 60


@dataclass
class Metrics:
    user_metrics: UserMetrics
    endpoint_metrics: EndpointMetrics
    rate_limit_metrics: RateLimitMetrics


@dataclass
class Request:
    user_id: int
    endpoint: str
    allowed: bool
    response_time: float


class MetricCollector:
    def __init__(self) -> None:
        self._user_metrics = UserMetrics()
        self._rate_limit_metrics = RateLimitMetrics()
        self._endpoint_metrics = EndpointMetrics()
        self._lock = threading.Lock()

    def record_request(
        self, user_id: int, endpoint: str, allowed: bool, response_time: float
    ) -> None:
        with self._lock:
            return Request(
                user_id=user_id,
                endpoint=endpoint,
                allowed=allowed,
                response_time=response_time,
            )

    def collect_all_metrics(self) -> Metrics:
        with self._lock:
            user_metrics = [
                UserMetrics(
                    user_id,
                    requests_count,
                    blocked_count,
                    last_request_time,
                    avg_requests_per_minute,
                )
                for user_id, requests_count, blocked_count, last_request_time, avg_requests_per_minute in self._user_metrics
            ]
            rate_limit_metrics = [
                RateLimitMetrics(
                    total_requests,
                    allowed_requests,
                    blocked_requests,
                    redis_errors,
                    avg_response_time,
                    active_users,
                )
                for total_requests, allowed_requests, blocked_requests, redis_errors, avg_response_time, active_users in self._rate_limit_metrics
            ]
            endpoint_metrics = [
                EndpointMetrics(
                    endpoint, total_requests, blocked_requests, unique_users
                )
                for endpoint, total_requests, blocked_requests, unique_users in self._endpoint_metrics
            ]
            return Metrics(
                user_metrics=user_metrics,
                endpoint_metrics=endpoint_metrics,
                rate_limit_metrics=rate_limit_metrics,
            )


class SimpleRateLimiter:
    def __init__(self):
        self._redis_config = RedisConfig()
        self._redis = redis.Redis(
            db=self._redis_config.db,
            host=self._redis_config.host,
            port=self._redis_config.port,
        )
        self._lock = threading.Lock()
        self._user_configs: Dict[str, UserLimitConfig] = {}
        self._metrics_collector: MetricCollector = MetricCollector()

    def set_user_config(self, user_id: str, config: UserLimitConfig):
        with self._lock:
            self._user_configs.update({user_id: config})
            logger.info(
                f"Config set for {user_id}: {config.max_requests} req/{config.window_seconds}s"
            )

    def is_allowed(self, user_id: str, endpoint: str = "default") -> bool:
        allowed: bool = False
        if config := self._user_configs.get(user_id):
            key = f"rate_limit:{user_id}:{endpoint}"
        else:
            raise UserConfigNotFoundError()

        current_time = time.time()
        window_start = current_time - config.window_seconds

        try:
            with self._lock:
                pipe = self._redis.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.expire(key, config.window_seconds)
                current_requests = pipe.execute()
                if current_requests[1] >= config.max_requests:
                    allowed = False
                    logger.warning(f"Rate limit exceeded for {user_id}")
                    return allowed

                allowed = True
                logger.info(
                    f"Request allowed for {user_id}, remaining: {config.max_requests - current_requests[1] - 1}"
                )
                return allowed

        except redis.RedisError as e:
            logger.error(f"Redis error: {e}")
            return allowed
        finally:
            self._metrics_collector.record_request(
                user_id=user_id,
                endpoint="default",
                allowed=allowed,
                response_time=window_start,
            )
