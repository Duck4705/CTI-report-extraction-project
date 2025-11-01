from .mapping_tool import map_sentence_with_IOC_CE

# Test case với sentence bị lỗi trước đây
sentence = "In some cases, Hive actors have bypassed multifactor authentication (MFA) and gained access to FortiOS servers by exploiting Common Vulnerabilities and Exposures (CVE) CVE-2020-12812."

# IOC dict - CVE phải được map đúng là CVE chứ không phải SoftwareTool  
ioc_dict = {
    "CVE": ["CVE-2020-12812"]  # CVE phải ở IOC
}

# CE dict - chú ý "Hive actors" dài hơn "Hive" nên sẽ được ưu tiên map trước
ce_dict = {
    "AttackGroup": ["Hive actors", "Hive"], 
    "SoftwareTool": ["FortiOS"]
}

mapped_sentence = map_sentence_with_IOC_CE(sentence, ioc_dict, ce_dict)
print("Original:", sentence)
print("Mapped  :", mapped_sentence)
print()

# Test case khác với BlackSuit
sentence2 = "BlackSuit shares numerous coding similarities with Royal ransomware and has exhibited improved capabilities. BlackSuit conducts data exfiltration."

ioc_dict2 = {}

ce_dict2 = {
    "AttackGroup": ["BlackSuit", "Royal"],
    "SoftwareTool": ["ransomware"]
}

mapped_sentence2 = map_sentence_with_IOC_CE(sentence2, ioc_dict2, ce_dict2)
print("Original:", sentence2) 
print("Mapped  :", mapped_sentence2)