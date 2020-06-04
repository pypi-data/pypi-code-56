from DKConnection import DKConnection

conn = DKConnection("cloud.datakitchen.io", "armand+hm@datakitchen.io", "%Gun8D9M")
testResults = conn.OrderRunInfo("hemonc_prod", 'b7ddd4fa-a20c-11ea-b702-6ebc574dfcbb')
testResults.test_by_type(testResults, "Warning")