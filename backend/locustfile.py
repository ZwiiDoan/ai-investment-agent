from locust import HttpUser, between, task


class FastAPIUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def ai_response_async(self):
        prompt = "test prompt"
        self.client.get("/ai-response", params={"prompt": prompt})

    # @task(1)
    # def ai_response_sync(self):
    #     prompt = "test prompt"
    #     self.client.get("/ai-response-sync", params={"prompt": prompt})
