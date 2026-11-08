// load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

// ============================================================
// Профиль нагрузки выбирается через переменную окружения:
//   k6 run load_test.js                    -> профиль A (10 VUs, 30s)
//   k6 run -e PROFILE=B load_test.js       -> профиль B (50 VUs, 10s)
// ============================================================

const PROFILE = __ENV.PROFILE || 'A';

const profiles = {
    A: {
        vus: 10,
        duration: '30s',
    },
    B: {
        vus: 50,
        duration: '10s',
    },
};

export const options = {
    ...profiles[PROFILE],
    thresholds: {
        // 95% запросов должны завершаться быстрее 500 мс
        http_req_duration: ['p(95)<500'],
        // Доля ошибок должна быть менее 1%
        http_req_failed: ['rate<0.01'],
    },
};

const BASE_URL = 'https://test-api.k6.io/public/crocodiles/';

export default function () {
    const res = http.get(BASE_URL);

    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
        'body is not empty': (r) => r.body.length > 0,
    });

    // Пауза между итерациями, имитирующая поведение пользователя
    sleep(1);
}