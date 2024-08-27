package com.example.study.cafe.service;

import com.example.study.cafe.repository.CafeRepository;
import com.example.study.cafe.api.dto.DocumentDto;
import com.example.study.cafe.api.dto.KakaoApiResponseDto;
import com.example.study.cafe.api.service.KakaoAddressCoordinateService;
import com.example.study.cafe.api.service.KakaoNearbyPlacesService;
import com.example.study.cafe.dto.OutputDto;
import com.example.study.cafe.entity.Cafe;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.beans.factory.annotation.Value;

import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class CafeRecommendationService {

    private final KakaoAddressCoordinateService kakaoAddressCoordinateService;
    private final KakaoNearbyPlacesService kakaoNearbyPlacesService;
    private final CafeRepository directionRepository;
    private final Base62Service base62Service;
    private static final double RADIUS_KM = 10.0; // 반경 10 km
    private static final int MAX_SEARCH_COUNT = 3; // 약국 최대 검색 갯수
    private static final String ROAD_VIEW_BASE_URL = "https://map.kakao.com/link/roadview/";

    @Value("${cafe.recommendation.base.url}")
    private String baseUrl;
    public List<OutputDto> recommendCafeList(String address) {

        // 고객이 입력한 문자열을 좌표로 변경
        KakaoApiResponseDto addressResponse = getAddressCoordinate(address);
        if (addressResponse == null || addressResponse.getDocumentList().isEmpty()) {
            log.warn("No address found for input: {}", address);
            return Collections.emptyList();
        }

        // api에서 받은 값에서 documentDto 부분 가져오기
        DocumentDto inputAddress = addressResponse.getDocumentList().get(0);

        //좌표로 가까운 카페 찾기
        KakaoApiResponseDto cafeResponse = searchNearByCafes(inputAddress);
        if (cafeResponse == null || cafeResponse.getDocumentList().isEmpty()) {
            log.warn("No cafes found near address: {}", inputAddress.getAddressName());
            return Collections.emptyList();
        }

        //api에서 받은 값에서 documentDto 부분 가져오고 Cafe엔티티로 변경
        List<Cafe> cafeList = createCafes(inputAddress, cafeResponse);

        directionRepository.saveAll(cafeList);

        return cafeList.stream()
                .map(this::convertToOutputDto)
                .collect(Collectors.toList());
    }
    private KakaoApiResponseDto getAddressCoordinate(String address) {
        KakaoApiResponseDto response = kakaoAddressCoordinateService.convertAddressToCoordinates(address);

        if (response == null || CollectionUtils.isEmpty(response.getDocumentList())) {
            log.error("[CafeRecommendationService getAddressCoordinate fail] Input address: {}", address);
            return null;
        }

        return response;
    }

    private KakaoApiResponseDto searchNearByCafes(DocumentDto inputAddress) {
        KakaoApiResponseDto response = kakaoNearbyPlacesService.getNearbyCafes(inputAddress.getLatitude(), inputAddress.getLongtitude(), RADIUS_KM);

        if(Objects.isNull(response)) {
            log.error("[PharmacyRecommendationService recommendCafeList fail] Input cafeList: {}", response);
            return null;
        }
        return response;
    }
    private static List<Cafe> createCafes(DocumentDto inputAddress, KakaoApiResponseDto cafeResponse) {
        return cafeResponse.getDocumentList().stream()
                .map(item -> Cafe.builder()
                                .inputAddress(inputAddress.getAddressName())
                                .inputLatitude(inputAddress.getLatitude())
                                .inputLongitude(inputAddress.getLongtitude())
                                .targetPharmacyName(item.getPalceName())
                                .targetLatitude(item.getLatitude())
                                .targetLongitude(item.getLongtitude())
                                .distance(item.getDistance() * 0.001)
                                .build())
                .limit(MAX_SEARCH_COUNT)
                .collect(Collectors.toList());
    }


    //결과 화면으로 뿌려주기 위한 정보들(outputDto)로 변환
    private OutputDto convertToOutputDto(Cafe cafeList) {

        return OutputDto.builder()
                .pharmacyName(cafeList.getTargetPharmacyName())
                .pharmacyAddress(cafeList.getTargetAddress())
                .directionUrl(baseUrl + base62Service.encodeDirectionId(cafeList.getId()))
                //로드뷰 URL + 위도 + 경도 (Direction엔티티에서 가져온다)
                .roadViewUrl(ROAD_VIEW_BASE_URL + cafeList.getTargetLatitude() + "," + cafeList.getTargetLongitude())
                .distance(String.format("%.2f km", cafeList.getDistance()))
                .build();
    }

}
