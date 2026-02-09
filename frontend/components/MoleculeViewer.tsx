
"use client";

import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, Sphere, Cylinder } from '@react-three/drei';
import * as THREE from 'three';

const Atom = ({ position, color, size = 0.4 }: { position: [number, number, number], color: string, size?: number }) => {
    return (
        <Sphere args={[size, 32, 32]} position={position}>
            <meshStandardMaterial
                color={color}
                roughness={0.1}
                metalness={0.3}
                emissive={color}
                emissiveIntensity={0.2}
            />
        </Sphere>
    );
};

const Bond = ({ start, end }: { start: [number, number, number], end: [number, number, number] }) => {
    const startVec = new THREE.Vector3(...start);
    const endVec = new THREE.Vector3(...end);
    const direction = new THREE.Vector3().subVectors(endVec, startVec);
    const length = direction.length();

    // Calculate position (midpoint)
    const position = new THREE.Vector3().addVectors(startVec, endVec).multiplyScalar(0.5);

    // Calculate rotation
    const quaternion = new THREE.Quaternion();
    quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.normalize());
    const rotation = new THREE.Euler().setFromQuaternion(quaternion);

    return (
        <group position={position} rotation={rotation}>
            <Cylinder args={[0.08, 0.08, length, 8]}>
                <meshStandardMaterial color="#94a3b8" transparent opacity={0.6} />
            </Cylinder>
        </group>
    );
};

const RotatingMolecule = () => {
    const groupRef = useRef<THREE.Group>(null);

    useFrame((state, delta) => {
        if (groupRef.current) {
            groupRef.current.rotation.y += delta * 0.2;
            groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
        }
    });

    // Mock "Imatinib-ish" Structure
    const atoms = [
        { pos: [0, 0, 0], color: "#e2e8f0" }, // C
        { pos: [1.2, 0.5, 0], color: "#e2e8f0" }, // C
        { pos: [-1.2, -0.5, 0.2], color: "#06b6d4" }, // N (Clinical Blue)
        { pos: [0.5, 1.5, -0.5], color: "#be123c" }, // O (Maroon danger hint)
        { pos: [-0.8, 1.0, 0.5], color: "#e2e8f0" },
        { pos: [2.0, -0.2, -0.5], color: "#e2e8f0" },
    ];

    const bonds = [
        [0, 1], [0, 2], [0, 4], [1, 3], [1, 5]
    ];

    return (
        <group ref={groupRef}>
            {atoms.map((atom, i) => (
                <Atom key={i} position={atom.pos as [number, number, number]} color={atom.color} />
            ))}
            {bonds.map((bond, i) => (
                <Bond key={i} start={atoms[bond[0]].pos as [number, number, number]} end={atoms[bond[1]].pos as [number, number, number]} />
            ))}
        </group>
    );
};

export default function MoleculeViewer() {
    return (
        <div className="w-full h-full relative">

            <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#06b6d4" />
                <spotLight position={[-10, -10, -10]} angle={0.3} intensity={0.5} color="#ec4899" />

                <RotatingMolecule />

                <OrbitControls enableZoom={false} autoRotate={false} />
                <Environment preset="city" />
            </Canvas>
        </div>
    );
}
