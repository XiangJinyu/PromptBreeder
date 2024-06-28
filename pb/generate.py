from concurrent.futures import ThreadPoolExecutor, as_completed

def generate(client, prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    return response.choices[0].message.content

def parallel_generate(client, prompts):
    with ThreadPoolExecutor() as executor:
        # 使用字典推导式创建future和prompt的映射
        future_to_prompt = {executor.submit(generate, client, prompt): prompt for prompt in prompts}
        results = []
        for future in as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                # 将生成的结果添加到结果列表中
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{prompt} generated an exception: {exc}')
    return results