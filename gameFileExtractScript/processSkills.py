import json
from common import *


def load_file_from_guid(ability_guid, suffix=None):
    filepath = guidToFilenames[ability_guid['guid']]
    if suffix:
        filepath = filepath.replace(".prefab", suffix + ".prefab")
    return load_yaml_file_with_tag_error(filepath)


with open("generatedAssets/skillTreesExtract.yaml", "r") as yamlFile:
    skillTreesData = yaml.safe_load(yamlFile)['trees'].values()

with open("generatedAssets/guidToFilenames.yaml", "r", encoding='utf-8') as yamlFile:
    guidToFilenames = yaml.safe_load(yamlFile)

skills = {
}

for skillTreeData in skillTreesData:
    skillData = load_file_from_guid(skillTreeData['ability'])["MonoBehaviour"]
    if skillData.get('playerAbilityID'):
        skill = {
            "name": skillData['abilityName'],
            "skillTypeTags": skillData['tags'],
            "baseFlags": {},
            "stats": [],
            "level": []
        }
        for prefabSuffix in {"", "End"}:
            skillPrefabData = load_file_from_guid(skillData['abilityPrefab'], prefabSuffix)
            for data in skillPrefabData:
                if data.get('MonoBehaviour') and data['MonoBehaviour'].get('baseDamageStats'):
                    skillDamageData = data['MonoBehaviour']['baseDamageStats']
                    if skillDamageData['isHit'] == "1":
                        skill["baseFlags"]["hit"] = True
                    match int(data['MonoBehaviour']['damageTags']):
                        case 256:
                            damageTag = "spell"
                            skill["baseFlags"]["spell"] = True
                        case 512:
                            damageTag = "melee"
                            skill["baseFlags"]["melee"] = True
                        case 1024:
                            damageTag = "throwing"
                            skill["baseFlags"]["projectile"] = True
                        case 2048:
                            damageTag = "bow"
                        case 4352:
                            damageTag = "dot"
                        case other:
                            damageTag = str(other)
                    for i, damageStr in enumerate(skillDamageData['damage']):
                        damage = float(damageStr)
                        if damage:
                            match i:
                                case 0:
                                    damageType = "physical"
                                case 1:
                                    damageType = "fire"
                                case 2:
                                    damageType = "cold"
                                case 3:
                                    damageType = "lightning"
                                case 4:
                                    damageType = "necrotic"
                                case 5:
                                    damageType = "void"
                                case _:
                                    damageType = "poison"
                            skill['stats'].append(damageTag + "_base_" + damageType + "_damage")
                            skill['level'].append(damage)
        skills[skillData['playerAbilityID']] = skill


skills = dict(natsorted(skills.items()))

with open("../src/Data/skills.json", "w") as jsonFile:
    json.dump(skills, jsonFile, indent=4)

print("skills processed with success")