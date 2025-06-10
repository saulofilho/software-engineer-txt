# Guia Completo de Red Hat

Este guia apresenta, em nível avançado, o **Red Hat Enterprise Linux (RHEL)** e o ecossistema da Red Hat para ambientes corporativos, cobrindo arquitetura, instalação, gerenciamento de pacotes, segurança, automação, contêineres e boas práticas.

---

## 1. Introdução ao Ecossistema Red Hat

* **Red Hat Enterprise Linux (RHEL)**: distribuição Linux corporativa com suporte comercial.
* **Projetos upstream**: Fedora (inovação rápida), CentOS Stream (pré-lançamento RHEL).
* **Produtos associados**:

  * **Red Hat Satellite**: gestão de ciclo de vida e patching de RHEL.
  * **Red Hat Ansible Automation Platform**: automação de TI.
  * **Red Hat OpenShift**: plataforma de contêineres Kubernetes.

---

## 2. Arquitetura e Edições do RHEL

* **Edições**:

  * **Server**: workloads genéricos.
  * **Workstation**: desktop corporativo.
  * **CoreOS**: minimal, para contêineres.
* **Suporte de Hardware**: certificações de ISVs e OEMs.
* **Modelos de Suporte**:

  * Standard (3 anos), Extended Life Cycle Support (ELS).

---

## 3. Instalação e Registro

### 3.1 Preparação

* Requisitos mínimos: 2 CPU, 4 GB RAM, 20 GB disco.
* Arquiteturas suportadas: x86\_64, ARM 64.

### 3.2 Instalação via ISO

1. **Download** do RHEL ISO no Customer Portal.
2. **Criar mídia**: `dd` ou ferramentas de gravação.
3. **Passos**:

   * Selecionar idioma e layout de teclado.
   * Configurar rede e hostname.
   * Particionamento (LVM recomendado).
   * Selecionar pacotes e Add-ons (Developer Tools, Virtualization).

### 3.3 Registro e Subscrição

```bash
subscription-manager register --username user --password pass
subscription-manager attach --pool=<POOL_ID>
subscription-manager repos --enable=rhel-8-for-x86_64-appstream-rpms
```

* **Pools**: IDs de subscrição para diferentes conjuntos de repos.
* **Repos**: AppStream, BaseOS, Extras, Supplementary.

---

## 4. Gestão de Pacotes com DNF/YUM

* **DNF** em RHEL 8+: transacional, depsolver melhorado.
* **Comandos**:

  * `dnf install <pkg>`, `dnf update`, `dnf remove`.
  * `dnf module list`, `dnf module enable <stream>` para AppStream modules.
  * `dnf config-manager` para gerenciar repositorios.
  * `dnf history` para reverter transações.

---

## 5. Administração de Sistema

### 5.1 Systemd e Serviços

* Gerenciar unidades:

  ```bash
  systemctl start|stop|restart <service>
  systemctl enable|disable <service>
  systemctl status <service>
  ```
* Logs com **journalctl**:

  ```bash
  journalctl -u <service> -f
  journalctl --since today
  ```

### 5.2 Gerenciamento de Usuários e Permissões

* **Users/Groups**: `useradd`, `usermod`, `groupadd`.
* **Sudo**: configurar em `/etc/sudoers.d/` via `visudo`.
* **Control Groups (cgroups)**: limitar recursos por usuário ou serviço.

### 5.3 Rede e Firewall

* **NetworkManager**: `nmcli`, `nmtui` para configurar conexões.
* **Firewalld** (default): zonas e serviços.

  ```bash
  firewall-cmd --zone=public --add-service=http --permanent
  firewall-cmd --reload
  ```

### 5.4 Armazenamento

* **LVM**: criar physical volumes, volume groups, logical volumes.
* **XFS** (default): tuning e quotas de projetos.
* **Multipath** para storage corporativo.
* **NVMe**: ajuste de scheduler I/O (mq-deadline ou none).

---

## 6. Segurança e Hardening

### 6.1 SELinux

* Modos: `Enforcing`, `Permissive`, `Disabled`.
* Ferramentas: `sestatus`, `semanage`, `audit2allow`, `restorecon`.
* Práticas:

  * Nunca desabilitar, usar permissive para debug.
  * Definir contextos corretos em volumes montados.

### 6.2 PAM e Políticas de Senha

* Arquivos: `/etc/pam.d/system-auth`, `/etc/security/pwquality.conf`.
* Configurar complexidade e histórico de senhas.

### 6.3 STIG e CIS Benchmarks

* Utilizar Ansible playbooks para conformidade.
* Auditorias automatizadas com **OpenSCAP**.

  ```bash
  oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_standard /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml
  ```

---

## 7. Virtualização e Contêineres

### 7.1 KVM/QEMU

* Pacotes: `@virt`, `libvirt`, `virt-install`, `virt-manager`.
* Gerenciar VMs:

  ```bash
  virsh list --all
  virt-install --name vm1 --memory 2048 --vcpus 2 --disk size=20 --cdrom /iso/rhel.iso
  ```
* Redes: NAT, bridge.

### 7.2 Contêineres com Podman

* Substituto rootless para Docker.

  ```bash
  podman pull registry.redhat.io/rhel8/httpd-24
  podman run -d -p 8080:80 httpd-24
  ```
* **Builds** com `buildah`, orquestração com `podman generate kube`.

---

## 8. Automação com Ansible

* **Ansible modules** para RHEL: `yum`, `subscription_manager`, `selinux`, `firewalld`.
* **Inventário dinâmico**: Satellite, AWS, etc.
* **Galaxy roles** oficiais da Red Hat.

---

## 9. Gerenciamento de Ciclo de Vida: Satellite

* **Red Hat Satellite**: provisioning PXE, patch management, config management.
* **Katello** plugin: gerencia conteúdo (repos, errata).
* **Provisioning**: hosts, activation keys, content views.

---

## 10. Observabilidade e Diagnóstico

* **Performance Co-Pilot (PCP)**, **tuned** profiles.
* **Metrics**: **Prometheus Node Exporter**, **Grafana**.
* **Tracing**: **LTTng**, **systemtap**.

---

## 11. Atualizações e Patching

* **Leapp** para upgrades in-place (RHEL 7→8).
* **dnf upgrade**, errata com `yum update --advisory=RHSA-xxxx:xxxx`.
* **Satellite** ou **Ansible** para escala.

---

## 12. Boas Práticas e Considerações Finais

1. **Mantenha subscrição ativa** para updates de segurança.
2. **Automatize auditorias** regulares com OpenSCAP.
3. **Use containers rootless** para isolamento.
4. **Aplique políticas SELinux** desde o design.
5. **Implemente CI/CD** para entrega de configs (Ansible).
6. **Monitore métricas** de host e aplicações.
7. **Teste upgrades** em ambientes isolados.
8. **Documente processos** e armazene em repositório Git.

---

## Conclusão

O ecossistema Red Hat oferece soluções robustas para ambientes corporativos, desde o sistema operacional até automação e orquestração de contêineres. Seguindo as práticas apresentadas, você garantirá segurança, escalabilidade e eficiência operacional.
