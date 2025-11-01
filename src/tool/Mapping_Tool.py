import re

def map_sentence_with_IOC_CE(sentence, ioc_dict, ce_dict):
    # IOC mapping: thay thế trực tiếp các IOC trong câu bằng loại của chúng
    all_iocs = []
    for ioc_type, ioc_list in ioc_dict.items():
        for ioc in ioc_list:
            all_iocs.append((ioc, ioc_type))
    
    # Sắp xếp IOCs theo độ dài giảm dần để map các chuỗi dài trước
    all_iocs.sort(key=lambda x: len(x[0]), reverse=True)
    
    for ioc, ioc_type in all_iocs:
        # Thay thế tất cả occurrences của IOC
        sentence = sentence.replace(ioc, ioc_type)
    
    # CE mapping: thêm chú thích vào các thực thể CE
    ce_explanation = {
        "AttackGroup": "This is Attack Group", 
        "SoftwareTool": "This is Software Tool"
    }
    
    all_ces = []
    for ce_type, ce_list in ce_dict.items():
        for ce in ce_list:
            all_ces.append((ce, ce_type))
    
    # Sắp xếp CEs theo độ dài giảm dần để map các chuỗi dài trước (ví dụ: "Hive actors" trước "Hive")
    all_ces.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Sử dụng set để track những gì đã được mapped
    mapped_entities = set()
    
    for ce, ce_type in all_ces:
        # Kiểm tra xem entity này có bị overlap với entity đã map chưa
        should_map = True
        for mapped_entity in mapped_entities:
            if ce in mapped_entity or mapped_entity in ce:
                should_map = False
                break
        
        if should_map and ce in sentence:
            # Chỉ map nếu chưa có annotation
            if f"{ce}(This is" not in sentence:
                replacement = f"{ce}({ce_explanation.get(ce_type, ce_type)})"
                sentence = sentence.replace(ce, replacement, 1)  # Chỉ thay thế lần đầu tiên
                mapped_entities.add(ce)
    
    return sentence