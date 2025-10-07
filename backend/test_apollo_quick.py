#!/usr/bin/env python3
"""
Script rápido para probar Apollo API con triario.com
"""

import requests
import json

def test_apollo_quick():
    """Prueba rápida de Apollo API"""
    print("🔍 Probando Apollo API con triario.com...")
    
    url = "https://api.apollo.io/api/v1/organizations/enrich"
    headers = {
        'x-api-key': 'ATpjar6DGtZOKVJWSTiGXQ',
        'accept': 'application/json'
    }
    params = {'domain': 'triario.com'}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            org = data.get('organization', {})
            
            print("✅ Apollo API funciona correctamente")
            print(f"📋 Empresa: {org.get('name', 'N/A')}")
            print(f"🏢 Industria: {org.get('industry', 'N/A')}")
            print(f"👥 Empleados: {org.get('estimated_num_employees', 'N/A')}")
            print(f"🌐 Sitio web: {org.get('website_url', 'N/A')}")
            
            # Mostrar tecnologías
            keywords = org.get('keywords', [])
            if keywords:
                print(f"💻 Tecnologías: {', '.join(keywords[:5])}")
            
            # Mostrar empleados
            people = data.get('people', [])
            if people:
                print(f"👨‍💼 Empleados encontrados: {len(people)}")
                for person in people[:3]:
                    name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                    title = person.get('title', 'N/A')
                    print(f"   - {name}: {title}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_apollo_quick()
