import csv
from ping3 import ping

def ping_site(host):
    response = ping(host, timeout=4)
    if response is not None:
        return "Доступен", response
    else:
        return "Недоступен", None
def save_to_csv(results, filename="/home/novip/compseti/1lab/result.csv"):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Сайт", "Статус", "Время ответа (мс)"]) 
        for site, (status, response_time) in results.items():
            writer.writerow([site, status, response_time if response_time is not None else "N/A"])

def main():
    sites = ["google.com", "youtube.com", "github.com", "ya.ru", "discord.com"]

    results = {}
    for site in sites:
        status, response_time = ping_site(site)  
        results[site] = (status, response_time) 

    save_to_csv(results)
    print(f"Результаты сохранены в файл")

if __name__ == "__main__":
    main()
