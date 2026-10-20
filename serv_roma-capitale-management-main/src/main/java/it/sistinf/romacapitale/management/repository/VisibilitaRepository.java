package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.VisibilitaEntity;
import org.springframework.stereotype.Repository;

@Repository
public class VisibilitaRepository extends AbstractRepository<Long, VisibilitaEntity> {

    public VisibilitaRepository() {
        super(VisibilitaEntity.class);
    }
}
