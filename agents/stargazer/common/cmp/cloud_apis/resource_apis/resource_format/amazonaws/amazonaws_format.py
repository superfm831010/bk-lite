# -*- coding: utf-8 -*-
from common.cmp.cloud_apis.cloud_object.base import (
    VM,
    VPC,
    Disk,
    Image,
    Region,
    SecurityGroup,
    SecurityGroupRule,
    Snapshot,
    Subnet,
    Zone,
)
from common.cmp.cloud_apis.resource_apis.resource_format.amazonaws.amazonaws_format_utils import (
    format_image_state,
    format_is_attached,
    format_region_status,
    format_rule_direction,
    format_rule_protocol,
    format_snapshot_status,
    format_tag,
    format_vm_status,
    format_volume_category,
    format_volume_status,
    format_vpc_status,
    handle_time_str,
)
from common.cmp.cloud_apis.resource_apis.resource_format.common.common_format import FormatResource


class AmazonAwsFormatResource(FormatResource):
    def __init__(self, region_id="", zone_id="", project_id="", cloud_type=""):
        self.zone_id = zone_id
        self.region_id = region_id
        self.project_id = project_id
        self.cloud_type = cloud_type

    def __new__(cls, *args, **kwargs):
        return super(AmazonAwsFormatResource, cls).__new__(cls, *args, **kwargs)

    def format_region(self, object_json, **kwargs):
        return Region(
            status=format_region_status(object_json.get("optInStatus", "available")),
            resource_id=object_json["regionName"],
            resource_name=object_json["regionName"],
            cloud_type=self.cloud_type,
            extra={"regionEndpoint": object_json.get("regionEndpoint", "")},
        ).to_dict()

    def format_zone(self, object_json, **kwargs):
        # 可用区无状态值
        # region_id
        return Zone(
            region=self.region_id,
            status="",
            resource_id=object_json["zoneId"],
            cloud_type=self.cloud_type,
            resource_name=object_json["zoneName"],
        ).to_dict()

    def format_vm(self, object_json, **kwargs):
        """
        虚拟机格式转换
        response elements
        amiLaunchIndex  Type: Integer
        architecture    Type: String    Valid Values: i386 | x86_64 | arm64 | x86_64_mac
        blockDeviceMapping  Type: Array of InstanceBlockDeviceMapping objects
            deviceName  Type: String
            ebs         Type: EbsInstanceBlockDevice object
                attachTime  Type: Timestamp
                deleteOnTermination     Type: Boolean
                status  Type: String    Valid Values: attaching | attached | detaching | detached
                volumeId    Type: String
        bootMode    Type: String    Valid Values: legacy-bios | uefi
        capacityReservationId   Type: String
        capacityReservationSpecification    Type: CapacityReservationSpecificationResponse object
            capacityReservationPreference   Type: String    Valid Values: open | none
            capacityReservationTarget      Type: CapacityReservationTargetResponse object
                capacityReservationId   Type: String
                capacityReservationResourceGroupArn     Type: String
        clientToken     Type: String
        cpuOptions      Type: CpuOptions object
            coreCount       Type: Integer
            threadsPerCore  Type: Integer
        dnsName         Type: String    IPv4 only
        ebsOptimized    Type: Boolean
        elasticGpuAssociationSet        Type: Array of ElasticGpuAssociation objects
            elasticGpuAssociationId     Type: String
            elasticGpuAssociationState      Type: String
            elasticGpuAssociationTime       Type: String
            elasticGpuId        Type: String
        elasticInferenceAcceleratorAssociationSet   Type: Array of ElasticInferenceAcceleratorAssociation objects
            elasticInferenceAcceleratorArn      Type: String
            elasticInferenceAcceleratorAssociationId    Type: String
            elasticInferenceAcceleratorAssociationState     Type: String
            elasticInferenceAcceleratorAssociationTime      Type: Timestamp
        enaSupport  Type: Boolean
        enclaveOptions  Type: EnclaveOptions object
            enabled     Type: Boolean
        groupSet    Type: Array of GroupIdentifier objects
            GroupId     Type: String
            GroupName   Type: String
        hibernationOptions      Type: HibernationOptions object
            configured      Type: Boolean
        hypervisor      Type: String
            Valid Values: ovm | xen
        iamInstanceProfile      Type: IamInstanceProfile object
            arn     Type: String
            id      Type: String
        imageId     Type: String
        instanceId      Type: String
        instanceLifecycle       Type: String    Valid Values: spot | scheduled
        instanceState    Type: InstanceState object
            code    Type: Integer
            name    Type: String
        instanceType    Type: String
        ipAddress   Type: String
        ipv6Address     Type: String
        kernelId        Type: String
        keyName         Type: String
        launchTime      Type: Timestamp
        licenseSet      Type: Array of LicenseConfiguration objects
            licenseConfigurationArn     Type: String
        maintenanceOptions      Type: InstanceMaintenanceOptions object
            autoRecovery        Type: String    Valid Values: disabled | default
        metadataOptions     Type: InstanceMetadataOptionsResponse object
            httpEndpoint        Type: String    Valid Values: disabled | enabled
            httpProtocolIpv6    Type: String    Valid Values: disabled | enabled
            httpPutResponseHopLimit     Type: Integer   Default: 1  values: 1 to 64
            httpTokens      Type: String    Default: optional   Valid Values: optional | required
            instanceMetadataTags    Type: String    Valid Values: disabled | enabled
            state       Type: String    Valid Values: pending | applied
        monitoring  Type: Monitoring object

        networkInterfaceSet     Type: Array of InstanceNetworkInterface objects

        outpostArn      Type: String
        placement       Type: Placement object

        platform        Type: String    Valid Values: Windows otherwise blank.
        platformDetails     Type: String
        privateDnsName      Type: String
        privateDnsNameOptions       Type: PrivateDnsNameOptionsResponse object

        privateIpAddress    Type: String
        productCodes        Type: Array of ProductCode objects

        ramdiskId   Type: String
        reason      Type: String
        rootDeviceName      Type: String
        rootDeviceType      Type: String    Valid Values: ebs | instance-store
        sourceDestCheck     Type: Boolean
        spotInstanceRequestId       Type: String
        sriovNetSupport     Type: String
        stateReason         Type: StateReason object

        subnetId        Type: String
        tagSet          Type: Array of Tag objects
        tpmSupport      Type: String
        usageOperation      Type: String
        usageOperationUpdateTime    Type: Timestamp
        virtualizationType      Type: String    Valid Values: hvm | paravirtual
        vpcId       Type: String
        """
        # disk_list = []
        object_json = object_json["instancesSet"]["item"]
        system_disk = []
        security_group_ids = []
        security_group_names = []
        # object_item = object_json["blockDeviceMapping"]
        # if type(object_item) is not list:
        #     object_item = [object_item]
        object_item = ""
        if object_json.get("blockDeviceMapping", ""):
            object_item = object_json["blockDeviceMapping"]["item"]
            if type(object_item) is not list:
                object_item = [object_item]
            for i in object_item:
                if i.get("ebs", []):
                    system_disk.append(i["ebs"]["volumeId"])
        if object_json.get("groupSet", ""):
            object_item = object_json["groupSet"]["item"]
            if type(object_item) is not list:
                object_item = [object_item]
            for i in object_item:
                security_group_ids.append(i["groupId"])
                security_group_names.append(i["groupName"])
        resource_name = ""
        sets = object_json.get("tagSet", {}).get("item", [])
        if type(sets) is not list:
            sets = [sets]
        for _set in sets:
            if _set.get("key") == "Name":
                resource_name = _set["value"]
                break
        return VM(
            resource_name=resource_name,
            cloud_type=self.cloud_type,
            resource_id=object_json["instanceId"],
            image=object_json.get("imageId", ""),
            os_name=object_json.get("platform", ""),
            status=format_vm_status(object_json["instanceState"].get("name", "")),
            instance_type=object_json.get("instanceType", ""),
            zone=object_json["placement"].get("availabilityZone", ""),
            subnet=object_json.get("subnetId", ""),
            vpc=object_json.get("vpcId", ""),
            inner_ip=object_json.get("privateIpAddress", []),
            public_ip=object_json.get("ipAddress", []),
            internet_accessible={},
            security_group=security_group_ids,
            vcpus=object_json["cpuOptions"].get("coreCount", ""),
            charge_type="",
            system_disk=system_disk,
            project=self.project_id,
            region=self.region_id,
            login_settings={},
            create_time=handle_time_str(object_json.get("launchTime", "")),
            expired_time="",
            peak_period=None,
            tag=format_tag(object_json.get("tagSet", "")),
            key_name=object_json.get("keyName", ""),
            extra={
                "security_group_name": security_group_names
                # to be added
            },
        ).to_dict()

    def format_disk(self, object_json, **kwargs):
        """
        response elements
        attachmentSet   Type: Array of VolumeAttachment objects
            attachTime      Type: Timestamp
            deleteOnTermination     Type: Boolean
            device          Type: String
            instanceId      Type: String
            status  Type: String    Valid Values: attaching | attached | detaching | detached | busy
            volumeId    Type: String
        availabilityZone    Type: String
        createTime      Type: Timestamp
        encrypted       Type: Boolean
        fastRestored    Type: Boolean
        iops            Type: Integer
        kmsKeyId        Type: String
        multiAttachEnabled      Type: Boolean
        outpostArn      Type: String
        size            Type: Integer   in GiBs.
        snapshotId      Type: String
        status      Type: String    Valid Values: creating | available | in-use | deleting | deleted | error
        tagSet      Type: Array of Tag objects
        throughput      Type: Integer       in MiB/s
        volumeId        Type: String
        volumeType      Type: String    Valid Values: standard | io1 | io2 | gp2 | sc1 | st1 | gp3
        """
        attach_time = ""
        if object_json.get("attachmentSet", ""):
            attach_time = object_json["attachmentSet"]["item"].get("attachTime", "")
        return Disk(
            cloud_type=self.cloud_type,
            resource_id=object_json["volumeId"],
            desc="",
            disk_size=object_json["size"],
            disk_type="",
            charge_type="",
            zone=object_json["availabilityZone"],
            status=format_volume_status(object_json["status"]),
            create_time=handle_time_str(attach_time),
            category=format_volume_category(object_json["volumeType"]),
            is_attached=format_is_attached(object_json.get("status", "")),
            encrypt=True if object_json.get("encrypted", "false") == "true" else False,
            snapshot_ability=object_json.get("fastRestored", False),
            project=self.project_id,
            region=self.region_id,
            tag=format_tag(object_json.get("tagSet", "")),
            extra={
                # to be added
            },
        ).to_dict()

    def format_vpc(self, object_json, **kwargs):
        """
        response elements
        cidrBlock   Type: String
        cidrBlockAssociationSet     Type: Array of VpcCidrBlockAssociation objects
            associationId   Type: String
            cidrBlock       Type: String
            cidrBlockState    Type: VpcCidrBlockState object
                state   Type: String
                ->Valid Values: associating | associated | disassociating | disassociated | failing | failed
                statusMessage   Type: String
        dhcpOptionsId   Type: String
        instanceTenancy     Type: String    Valid Values: default | dedicated | host
        ipv6CidrBlockAssociationSet     Type: Array of VpcIpv6CidrBlockAssociation objects
            associationId   Type: String
            ipv6CidrBlock   Type: String
            ipv6CidrBlockState     Type: VpcCidrBlockState object
                state   Type: String
                ->Valid Values: associating | associated | disassociating | disassociated | failing | failed
                statusMessage   Type: String
            ipv6Pool        Type: String
            networkBorderGroup      Type: String
        isDefault   Type: Boolean
        ownerId     Type: String
        state       Type: String    Valid Values: pending | available
        tagSet  Type: Array of Tag objects
        vpcId   The ID of the VPC.
        """

        return VPC(
            cloud_type=self.cloud_type,
            resource_id=object_json["vpcId"],
            resource_name="",
            router="",
            router_tables={},
            status=format_vpc_status(object_json.get("state", "")),
            cidr=object_json.get("cidrBlock", ""),
            cidr_v6=object_json["ipv6CidrBlockAssociationSet"]["ipv6CidrBlock"][0]
            if object_json.get("ipv6CidrBlockAssociationSet")
            else "",
            is_default=True if object_json.get("isDefault", "false") == "true" else False,
            project=self.project_id,
            zone=self.zone_id,
            region=self.region_id,
            desc="",
            tag=format_tag(object_json.get("tagSet", "")),
            extra={
                # to be added
            },
        ).to_dict()

    def format_subnet(self, object_json, **kwargs):
        """
        response elements
        assignIpv6AddressOnCreation     Type: Boolean
        availabilityZone    Type: String
        availabilityZoneId  Type: String
        availableIpAddressCount     Type: Integer
        cidrBlock       Type: String
        customerOwnedIpv4Pool   Type: String
        defaultForAz    Type: Boolean
        enableDns64     Type: Boolean
        enableLniAtDeviceIndex  Type: Integer
        ipv6CidrBlockAssociationSet     Type: Array of SubnetIpv6CidrBlockAssociation objects
            associationId   Type: String
            ipv6CidrBlock   Type: String
            ipv6CidrBlockState      Type: SubnetCidrBlockState object
                state   Type: String
                ->Valid Values: associating | associated | disassociating | disassociated | failing | failed
                statusMessage   Type: String
        ipv6Native  Type: Boolean
        mapCustomerOwnedIpOnLaunch  Type: Boolean
        mapPublicIpOnLaunch     Type: Boolean
        outpostArn      Type: String
        ownerId         Type: String
        privateDnsNameOptionsOnLaunch       Type: PrivateDnsNameOptionsOnLaunch object
            enableResourceNameDnsAAAARecord Type: Boolean
            enableResourceNameDnsARecord    Type: Boolean
            hostnameType        Type: String    Valid Values: ip-name | resource-name
        state   Type: String    Valid Values: pending | available
        subnetArn   Type: String
        subnetId    Type: String
        tagSet      Type: Array of Tag objects
        vpcId       Type: String
        """
        return Subnet(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("subnetId", ""),
            resource_name=object_json.get("subnetArn", "未命名"),
            vpc=object_json.get("vpcId", ""),
            status=format_vpc_status(object_json.get("state", "")),
            cidr=object_json.get("cidrBlock", ""),
            cidr_v6=object_json["ipv6CidrBlockAssociationSet"]["ipv6CidrBlock"][0]
            if object_json.get("ipv6CidrBlockAssociationSet")
            else "",
            zone=object_json.get("availabilityZoneId"),
            is_default=True if object_json.get("isDefault", "false") == "true" else False,
            tag=format_tag(object_json.get("tagSet", "")),
            region=self.region_id,
            desc="",
            extra={
                "availableIpAddressCount": object_json.get("AvailableIpAddressCount", ""),
                "availabilityZoneName": object_json.get("availabilityZone", ""),
                # to be added
                # "mapPublicIpOnLaunch": object_json.get("mapPublicIpOnLaunch", ""),
                # "assignIpv6AddressOnCreation": object_json.get("assignIpv6AddressOnCreation", "")
            },
        ).to_dict()

    def format_security_group(self, object_json, **kwargs):
        """
        response elements

        groupDescription    Type: String
        groupId     Type: String
        groupName   Type: String
        ipPermissions (inbound rules)  Type: Array of IpPermission objects (response lowercase)
            FromPort    Type: Integer
            UserIdGroupPairs    Type: Array of UserIdGroupPair objects
                Description     Type: String
                GroupId     Type: String
                GroupName   Type: String
                PeeringStatus   Type: String
                UserId      Type: String
                VpcId       Type: String
                VpcPeeringConnectionId      Type: String
            IpProtocol  Type: String
            IpRanges    Type: Array of IpRange objects
                CidrIp  Type: String
                Description     Type: String
            Ipv6Ranges      Type: Array of Ipv6Range objects
                CidrIpv6    Type: String
                Description     Type: String
            PrefixListIds   Type: Array of PrefixListId objects
                Description     Type: String
                PrefixListId    Type: String
            ToPort      Type: Integer
        ipPermissionsEgress (outbound rules)  Type: Array of IpPermission objects
        ownerId     Type: String
        tagSet      Type: Array of Tag objects
        vpcId
        """
        return SecurityGroup(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("groupId", ""),
            resource_name=object_json.get("groupName", "未命名"),
            desc=object_json.get("groupDescription", ""),
            vpc=object_json.get("vpcId", ""),
            tag=format_tag(object_json.get("tagSet", "")),
            resource_group="",
            zone=self.zone_id,
            extra={
                # to be added
            },
        ).to_dict()

    def format_security_group_rule(self, object_json, **kwargs):
        """
        response elements

        securityGroupRuleSet    Type: Array of SecurityGroupRule objects
            cidrIpv4    Type: String
            cidrIpv6    Type: String
            description     Type: String
            fromPort        Type: Integer
            groupId         Type: String
            groupOwnerId    Type: String
            ipProtocol      Type: String
            isEgress        Type: Boolean
            prefixListId    Type: String
            referencedGroupInfo     Type: ReferencedSecurityGroup object
            securityGroupRuleId     Type: String
            tagSet          Type: Array of Tag objects
            toPort          Type: Integer
        """
        return SecurityGroupRule(
            cloud_type=self.cloud_type,
            resource_id=object_json["securityGroupRuleId"],
            resource_name="未命名",
            direction=format_rule_direction(object_json.get("isEgress", "ERROR")),
            protocol=format_rule_protocol(object_json.get("ipProtocol", "-1")),
            security_group=kwargs.get("groupId", ""),
            desc=object_json.get("description", ""),
            port_range=f'{object_json.get("fromPort", "")},{object_json.get("toPort", "")}',
            tag=format_tag(object_json.get("Tags", "")),
            region=object_json.get("RegionId", self.region_id),
            zone=object_json.get("ZoneId", self.zone_id),
        ).to_dict()

    def format_snapshot(self, object_json, **kwargs):
        """
        response
        see https://docs.amazonaws.cn/AWSEC2/latest/APIReference/API_Snapshot.html

        dataEncryptionKeyId     Type: String
        description             Type: String
        encrypted               Type: Boolean
        kmsKeyId                Type: String
        outpostArn              Type: String
        ownerAlias              Type: String
        ownerId                 Type: String
        progress                Type: String
        restoreExpiryTime       Type: Timestamp
        snapshotId              Type: String
        startTime               Type: Timestamp
        status   Type: String   Valid Values: pending | completed | error | recoverable | recovering
        statusMessage   Type: String
        storageTier     Type: String    Valid Values: archive | standard
        tagSet          Type: Array of Tag objects
        volumeId        Type: String
        volumeSize      Type: Integer
        """
        return Snapshot(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("snapshotId", ""),
            resource_name=object_json.get("snapshotName", "未命名"),
            desc=object_json.get("description", "") or "",
            tag=format_tag(object_json.get("tagSet", "")),
            disk_id=object_json.get("volumeId", ""),
            disk_size=object_json.get("volumeSize", 0),
            status=format_snapshot_status(object_json.get("status", "")),
            create_time=handle_time_str(object_json.get("startTime", "")),
            region=self.region_id,
            zone=self.zone_id,
            encrypt=True if object_json.get("encrypted", "false") == "true" else False,
            extra={"Progress": object_json.get("Progress", "")},
        ).to_dict()

    def format_image(self, object_json, **kwargs):
        """
        response
        see     https://docs.amazonaws.cn/AWSEC2/latest/APIReference/API_DescribeImages.html

        architecture    Type: String    Valid Values: i386 | x86_64 | arm64 | x86_64_mac
        blockDeviceMapping   Type: Array of BlockDeviceMapping objects
            deviceName  Type: String
            ebs     Type: EbsBlockDevice object
                deleteOnTermination    Type: Boolean
                encrypted       Type: Boolean
                iops            Type: Integer
                KmsKeyId        Type: String
                outpostArn      Type: String
                snapshotId      Type: String
                throughput      Type: Integer
                volumeSize      Type: Integer
                volumeType      Type: String
                ->Valid Values: standard | io1 | io2 | gp2 | sc1 | st1 | gp3
            noDevice    Type: String
            virtualName     Type: String
        bootMode    Type: String   Valid Values: legacy-bios | uefi
        creationDate    Type: String
        deprecationTime     Type: String
        description    Type: String
        enaSupport      Type: Boolean
        hypervisor      Type: String    Valid Values: ovm | xen
        imageId         Type: String
        imageLocation       Type: String
        imageOwnerAlias     Type: String
        imageOwnerId        Type: String
        imageState          Type: String
        ->Valid Values: pending | available | invalid | deregistered | transient | failed | error
        imageType           Type: String    Valid Values: machine | kernel | ramdisk
        isPublic            Type: Boolean
        kernelId            Type: String
        name                Type: String
        platform            Type: String    Windows or blank.
        platformDetails     Type: String
        productCodes        Type: Array of ProductCode objects
            productCode     Type: String
            type            Type: String    Valid Values: devpay | marketplace
        ramdiskId           Type: String
        rootDeviceName      Type: String
        rootDeviceType      Type: String    Valid Values: ebs | instance-store
        sriovNetSupport     Type: String
        stateReason         Type: StateReason object
            code        Type: String
            message     Type: String
        tagSet          Type: Array of Tag objects
        tpmSupport      Type: String    Valid Values: v2.0
        usageOperation  Type: String
        virtualizationType  Type: String    Valid Values: hvm | paravirtual
        """
        size = 0
        if object_json.get("blockDeviceMapping", ""):
            size = sum(
                [int(item.get("ebs", {}).get("volumeSize", 0)) for item in object_json["blockDeviceMapping"]["item"]]
            )
        return Image(
            cloud_type=self.cloud_type,
            resource_id=object_json.get("imageId", ""),
            resource_name=object_json.get("name", "未命名"),
            desc=object_json.get("description", ""),
            tag=format_tag(object_json.get("tagSet")),
            arch=object_json.get("architecture", ""),
            platform=object_json.get("platform", ""),
            size=size,
            status=format_image_state(object_json.get("imageState", "")),
            create_time=handle_time_str(object_json.get("creationDate", "")),
            extra={
                "imageOwnerAlias": object_json.get("imageOwnerAlias", ""),
                "isPublic": object_json.get("isPublic", ""),
                "usageOperation": object_json.get("usageOperation", ""),
            },
        ).to_dict()
