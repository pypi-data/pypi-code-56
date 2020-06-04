import client

dot = client.Connect("user", "password",
                     "https://nsdb.domain.com", debug=0)

host = dot.get_host_by_name("your_host")

print(host)
