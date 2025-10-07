#!/usr/bin/env python3
"""
Script de prueba para el sistema de almacenamiento de conversaciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage.conversation_storage import conversation_storage
import json

def test_conversation_storage():
    """Prueba las funciones del sistema de almacenamiento"""
    
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE ALMACENAMIENTO")
    print("=" * 60)
    
    # Datos de prueba
    test_conversation_id = "test-conv-12345"
    test_hubspot_id = "hubspot-67890"
    test_prospect_data = {
        "nombres": "Juan",
        "apellidos": "Pérez",
        "compania": "Empresa Test",
        "websiteUrl": "https://empresatest.com",
        "emailCorporativo": "juan.perez@empresatest.com",
        "rol": "CEO"
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   - conversation_id: {test_conversation_id}")
    print(f"   - hubspot_id: {test_hubspot_id}")
    print(f"   - prospect_data: {json.dumps(test_prospect_data, indent=2)}")
    print()
    
    # 1. Probar almacenamiento
    print("1️⃣ PROBANDO ALMACENAMIENTO")
    print("-" * 30)
    
    success = conversation_storage.store_mapping(
        conversation_id=test_conversation_id,
        hubspot_id=test_hubspot_id,
        prospect_data=test_prospect_data
    )
    
    if success:
        print("✅ Almacenamiento exitoso")
    else:
        print("❌ Error en almacenamiento")
        return False
    
    print()
    
    # 2. Probar consulta completa
    print("2️⃣ PROBANDO CONSULTA COMPLETA")
    print("-" * 30)
    
    mapping = conversation_storage.get_mapping(test_conversation_id)
    if mapping:
        print("✅ Mapeo encontrado:")
        print(json.dumps(mapping, indent=2, ensure_ascii=False))
    else:
        print("❌ Mapeo no encontrado")
        return False
    
    print()
    
    # 3. Probar consulta de hubspot_id
    print("3️⃣ PROBANDO CONSULTA DE HUBSPOT_ID")
    print("-" * 30)
    
    retrieved_hubspot_id = conversation_storage.get_hubspot_id(test_conversation_id)
    if retrieved_hubspot_id == test_hubspot_id:
        print(f"✅ HubSpot ID correcto: {retrieved_hubspot_id}")
    else:
        print(f"❌ HubSpot ID incorrecto. Esperado: {test_hubspot_id}, Obtenido: {retrieved_hubspot_id}")
        return False
    
    print()
    
    # 4. Probar listado
    print("4️⃣ PROBANDO LISTADO")
    print("-" * 30)
    
    listings = conversation_storage.list_mappings(limit=10)
    if listings and "mappings" in listings:
        print(f"✅ Listado exitoso. Total: {listings['total_count']}, Retornados: {listings['returned_count']}")
        print("Mapeos encontrados:")
        for conv_id, mapping_data in listings["mappings"].items():
            print(f"   - {conv_id}: {mapping_data.get('hubspot_id', 'N/A')}")
    else:
        print("❌ Error en listado")
        return False
    
    print()
    
    # 5. Probar actualización
    print("5️⃣ PROBANDO ACTUALIZACIÓN")
    print("-" * 30)
    
    update_success = conversation_storage.update_mapping(
        test_conversation_id,
        notes="Actualización de prueba"
    )
    
    if update_success:
        updated_mapping = conversation_storage.get_mapping(test_conversation_id)
        if updated_mapping and updated_mapping.get("notes") == "Actualización de prueba":
            print("✅ Actualización exitosa")
        else:
            print("❌ Error verificando actualización")
            return False
    else:
        print("❌ Error en actualización")
        return False
    
    print()
    
    # 6. Probar consulta de conversation_id inexistente
    print("6️⃣ PROBANDO CONSULTA DE ID INEXISTENTE")
    print("-" * 30)
    
    non_existent_mapping = conversation_storage.get_mapping("non-existent-id")
    if non_existent_mapping is None:
        print("✅ Comportamiento correcto para ID inexistente")
    else:
        print("❌ Error: debería retornar None para ID inexistente")
        return False
    
    print()
    
    # 7. Limpiar datos de prueba
    print("7️⃣ LIMPIANDO DATOS DE PRUEBA")
    print("-" * 30)
    
    delete_success = conversation_storage.delete_mapping(test_conversation_id)
    if delete_success:
        print("✅ Datos de prueba eliminados")
        
        # Verificar que se eliminó
        deleted_mapping = conversation_storage.get_mapping(test_conversation_id)
        if deleted_mapping is None:
            print("✅ Verificación de eliminación exitosa")
        else:
            print("❌ Error: el mapeo debería estar eliminado")
            return False
    else:
        print("❌ Error eliminando datos de prueba")
        return False
    
    print()
    print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_conversation_storage()
    sys.exit(0 if success else 1)
